from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.quiz_list_view, name='quiz_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz_view, name='start_quiz'),
    path('quiz/<int:quiz_id>/', views.take_quiz_view, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit-answer/', views.submit_answer_view, name='submit_answer'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz_view, name='submit_quiz'),
    path('quiz/<int:quiz_id>/leaderboard/', views.leaderboard_view, name='quiz_leaderboard'),
    path('results/<int:submission_id>/', views.quiz_results_view, name='quiz_results'),
]

