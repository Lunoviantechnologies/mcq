from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, UserProfile


class UserRegistrationForm(UserCreationForm):
    """Custom registration form with category selection"""
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select at least one category to register for. You will only see quizzes from your selected categories."
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'categories']
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Get or create user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            # Add selected categories
            profile.registered_categories.set(self.cleaned_data['categories'])
        return user

