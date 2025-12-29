from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Quiz, Question, Choice, QuizSubmission, Answer, UserProfile
from .forms import UserRegistrationForm


def check_quiz_category_access(user, quiz):
    """Check if user has access to the quiz's category"""
    if not quiz.category:
        # If quiz has no category, allow access (for backward compatibility)
        return True
    
    try:
        user_profile = user.profile
        registered_categories = user_profile.registered_categories.all()
        return quiz.category in registered_categories
    except UserProfile.DoesNotExist:
        # If user has no profile, they have no registered categories
        return False


def register_view(request):
    """User registration view with category selection"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            categories = form.cleaned_data.get('categories')
            category_names = ', '.join([cat.name for cat in categories])
            messages.success(
                request, 
                f'Account created for {username}! Registered categories: {category_names}. You can now log in.'
            )
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'quiz_app/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('quiz_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('quiz_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'quiz_app/login.html')


@login_required
def quiz_list_view(request):
    """Display list of available quizzes filtered by user's registered categories"""
    # Get user's registered categories
    try:
        user_profile = request.user.profile
        registered_categories = user_profile.registered_categories.all()
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist (for existing users)
        user_profile = UserProfile.objects.create(user=request.user)
        registered_categories = user_profile.registered_categories.all()
    
    # Filter quizzes by user's registered categories
    if registered_categories.exists():
        quizzes = Quiz.objects.filter(
            is_active=True,
            category__in=registered_categories
        ).prefetch_related('submissions', 'questions', 'category')
    else:
        # If user has no registered categories, show no quizzes
        quizzes = Quiz.objects.none()
        messages.info(
            request, 
            'You have not registered for any categories. Please contact an administrator to register for categories.'
        )
    
    user_submissions = QuizSubmission.objects.filter(trainee=request.user, is_completed=True).select_related('quiz')
    submitted_quiz_ids = user_submissions.values_list('quiz_id', flat=True)
    
    # Create a dictionary mapping quiz_id to submission_id for easy lookup
    submission_map = {sub.quiz_id: sub.id for sub in user_submissions}
    
    context = {
        'quizzes': quizzes,
        'submitted_quiz_ids': list(submitted_quiz_ids),
        'submission_map': submission_map,
        'registered_categories': registered_categories,
    }
    return render(request, 'quiz_app/quiz_list.html', context)


@login_required
def start_quiz_view(request, quiz_id):
    """Start a quiz - create submission if doesn't exist"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # Check if user has access to this quiz's category
    if not check_quiz_category_access(request.user, quiz):
        messages.error(request, 'You do not have access to quizzes in this category.')
        return redirect('quiz_list')
    
    # Check if user already has a submission
    submission, created = QuizSubmission.objects.get_or_create(
        quiz=quiz,
        trainee=request.user,
        defaults={'started_at': timezone.now()}
    )
    
    if submission.is_completed:
        messages.info(request, 'You have already completed this quiz.')
        return redirect('quiz_results', submission_id=submission.id)
    
    return redirect('take_quiz', quiz_id=quiz_id)


@login_required
def take_quiz_view(request, quiz_id):
    """Display quiz questions for taking"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # Check if user has access to this quiz's category
    if not check_quiz_category_access(request.user, quiz):
        messages.error(request, 'You do not have access to quizzes in this category.')
        return redirect('quiz_list')
    
    submission = get_object_or_404(QuizSubmission, quiz=quiz, trainee=request.user)
    
    if submission.is_completed:
        messages.info(request, 'You have already completed this quiz.')
        return redirect('quiz_results', submission_id=submission.id)
    
    questions = quiz.questions.all()
    # total time in seconds based on per-question time limits
    total_time_seconds = sum(q.time_limit_minutes for q in questions) * 60
    existing_answers = {answer.question_id: answer for answer in submission.answers.all()}
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'submission': submission,
        'existing_answers': existing_answers,
        'total_time_seconds': total_time_seconds,
    }
    return render(request, 'quiz_app/take_quiz.html', context)


@login_required
@require_http_methods(["POST"])
def submit_answer_view(request, quiz_id):
    """Save an answer for a question"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Check if user has access to this quiz's category
    if not check_quiz_category_access(request.user, quiz):
        return JsonResponse({'error': 'You do not have access to quizzes in this category.'}, status=403)
    
    submission = get_object_or_404(QuizSubmission, quiz=quiz, trainee=request.user)
    
    if submission.is_completed:
        return JsonResponse({'error': 'Quiz already completed'}, status=400)
    
    question_id = request.POST.get('question_id')
    question = get_object_or_404(Question, id=question_id, quiz=quiz)
    
    answer, created = Answer.objects.get_or_create(
        submission=submission,
        question=question
    )
    
    if question.question_type == 'multiple_choice':
        choice_id = request.POST.get('choice_id')
        if choice_id:
            choice = get_object_or_404(Choice, id=choice_id, question=question)
            answer.selected_choice = choice
            answer.answer_text = choice.choice_text
    else:
        answer_text = request.POST.get('answer_text', '')
        answer.answer_text = answer_text
    
    answer.save()
    
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["POST"])
def submit_quiz_view(request, quiz_id):
    """Submit the entire quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Check if user has access to this quiz's category
    if not check_quiz_category_access(request.user, quiz):
        messages.error(request, 'You do not have access to quizzes in this category.')
        return redirect('quiz_list')
    
    submission = get_object_or_404(QuizSubmission, quiz=quiz, trainee=request.user)
    
    if submission.is_completed:
        return JsonResponse({'error': 'Quiz already completed'}, status=400)
    
    # Calculate score
    total_questions = quiz.questions.count()
    correct_answers = 0
    
    for answer in submission.answers.all():
        if answer.question.question_type == 'multiple_choice':
            if answer.selected_choice and answer.selected_choice.is_correct:
                correct_answers += 1
    
    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    submission.is_completed = True
    submission.submitted_at = timezone.now()
    submission.score = score
    submission.save()
    
    messages.success(request, f'Quiz submitted successfully! Your score: {score:.1f}%')
    return redirect('quiz_results', submission_id=submission.id)


@login_required
def quiz_results_view(request, submission_id):
    """Display quiz results"""
    submission = get_object_or_404(QuizSubmission, id=submission_id, trainee=request.user)
    quiz = submission.quiz
    
    # Check if user has access to this quiz's category
    if not check_quiz_category_access(request.user, quiz):
        messages.error(request, 'You do not have access to quizzes in this category.')
        return redirect('quiz_list')
    
    answers = submission.answers.select_related('question', 'selected_choice').all()
    
    # Create a dictionary for easy lookup
    answers_dict = {answer.question_id: answer for answer in answers}
    
    context = {
        'submission': submission,
        'quiz': quiz,
        'questions': quiz.questions.all(),
        'answers_dict': answers_dict,
    }
    return render(request, 'quiz_app/quiz_results.html', context)


@login_required
def leaderboard_view(request, quiz_id):
    """Display leaderboard for a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Check if user has access to this quiz's category
    if not check_quiz_category_access(request.user, quiz):
        messages.error(request, 'You do not have access to quizzes in this category.')
        return redirect('quiz_list')
    
    submissions = (
        QuizSubmission.objects.filter(quiz=quiz, is_completed=True, score__isnull=False)
        .select_related('trainee')
        .order_by('-score', 'submitted_at')[:50]
    )
    context = {
        'quiz': quiz,
        'submissions': submissions,
    }
    return render(request, 'quiz_app/leaderboard.html', context)


@staff_member_required
def user_list_view(request):
    """Admin/staff: list all registered users."""
    users = User.objects.all().order_by('date_joined')
    return render(request, 'quiz_app/user_list.html', {'users': users})


@staff_member_required
@require_http_methods(["POST"])
def delete_user_view(request, user_id):
    """Admin/staff: delete a user."""
    user_to_delete = get_object_or_404(User, id=user_id)

    # Safety checks
    if user_to_delete.id == request.user.id:
        messages.error(request, "You cannot delete your own account while logged in.")
        return redirect('user_list')
    if user_to_delete.is_superuser:
        messages.error(request, "You cannot delete a superuser from here.")
        return redirect('user_list')

    username = user_to_delete.username
    user_to_delete.delete()
    messages.success(request, f"User '{username}' deleted successfully.")
    return redirect('user_list')

