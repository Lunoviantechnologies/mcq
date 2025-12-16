from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('text', 'Text Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    order = models.IntegerField(default=0)
    time_limit_minutes = models.PositiveIntegerField(default=1, help_text="Time allowed for this question in minutes")
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order + 1}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.question} - {self.choice_text}"


class QuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_submissions')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ['quiz', 'trainee']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.trainee.username} - {self.quiz.title}"


class Answer(models.Model):
    submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ['submission', 'question']
    
    def __str__(self):
        if self.selected_choice:
            return f"{self.submission} - {self.question} - {self.selected_choice.choice_text}"
        return f"{self.submission} - {self.question} - {self.answer_text}"

