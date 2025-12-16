from django.contrib import admin
from .models import Quiz, Question, Choice, QuizSubmission, Answer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'order']
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'is_correct']
    list_filter = ['is_correct']


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'trainee', 'started_at', 'submitted_at', 'is_completed', 'score']
    list_filter = ['is_completed', 'submitted_at']
    search_fields = ['trainee__username', 'quiz__title']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['submission', 'question', 'selected_choice', 'answer_text']
    list_filter = ['submission__quiz']

