# Setup Instructions

## Quick Start

1. **Install Python** (if not already installed)
   - Python 3.8 or higher is required

2. **Install Django and dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Open your browser and go to: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Creating Sample Data

### Option 1: Using Django Admin

1. Log in to the admin panel at http://127.0.0.1:8000/admin/
2. Create a Quiz:
   - Go to "Quizzes" → "Add Quiz"
   - Enter a title (e.g., "Python Basics Quiz")
   - Enter a description (optional)
   - Select yourself as "Created by"
   - Click "Save"
3. Add Questions:
   - Go to "Questions" → "Add Question"
   - Select the quiz you created
   - Enter question text (e.g., "What is Python?")
   - Select question type (Multiple Choice or Text)
   - Set order (0 for first question, 1 for second, etc.)
   - Click "Save"
4. Add Choices (for multiple choice questions):
   - Go to "Choices" → "Add Choice"
   - Select the question
   - Enter choice text (e.g., "A programming language")
   - Check "Is correct" if this is the correct answer
   - Click "Save"
   - Repeat for all choices

### Option 2: Using Django Shell

You can also create sample data using the Django shell:

```bash
python manage.py shell
```

Then run:

```python
from django.contrib.auth.models import User
from quiz_app.models import Quiz, Question, Choice

# Get or create a user
user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
if created:
    user.set_password('admin123')
    user.save()

# Create a quiz
quiz = Quiz.objects.create(
    title='Sample Python Quiz',
    description='Test your Python knowledge',
    created_by=user,
    is_active=True
)

# Create questions
q1 = Question.objects.create(
    quiz=quiz,
    question_text='What is Python?',
    question_type='multiple_choice',
    order=0
)

# Create choices for question 1
Choice.objects.create(question=q1, choice_text='A snake', is_correct=False)
Choice.objects.create(question=q1, choice_text='A programming language', is_correct=True)
Choice.objects.create(question=q1, choice_text='A type of pie', is_correct=False)

q2 = Question.objects.create(
    quiz=quiz,
    question_text='What is Django?',
    question_type='multiple_choice',
    order=1
)

Choice.objects.create(question=q2, choice_text='A web framework', is_correct=True)
Choice.objects.create(question=q2, choice_text='A database', is_correct=False)
Choice.objects.create(question=q2, choice_text='A programming language', is_correct=False)

# Create a text question
q3 = Question.objects.create(
    quiz=quiz,
    question_text='Explain what you like about Python.',
    question_type='text',
    order=2
)

print("Sample quiz created successfully!")
```

## Testing the Application

1. **Register a new trainee account**:
   - Go to http://127.0.0.1:8000/register/
   - Create a new account

2. **Login**:
   - Go to http://127.0.0.1:8000/login/
   - Use your credentials

3. **Take a quiz**:
   - You'll see available quizzes on the home page
   - Click "Start Quiz"
   - Answer the questions
   - Click "Submit Quiz" when done
   - View your results

## Troubleshooting

### Database errors
If you get database errors, try:
```bash
python manage.py migrate --run-syncdb
```

### Static files not loading
If CSS/styles aren't loading:
```bash
python manage.py collectstatic
```

### Port already in use
If port 8000 is busy, use a different port:
```bash
python manage.py runserver 8001
```

