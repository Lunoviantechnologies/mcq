# Quick Start Guide - Django Quiz Application

## Project Directory
The project is located at: `C:\Users\yash\Desktop\HR`

## Prerequisites
- Python 3.8 or higher installed
- pip (Python package manager)

## Step-by-Step Setup

### Step 0: Create and Activate Virtual Environment (Recommended)

**Create virtual environment:**
```bash
python -m venv venv
```

**Activate virtual environment:**

On **Windows (PowerShell)**:
```bash
.\venv\Scripts\Activate.ps1
```

On **Windows (Command Prompt)**:
```bash
venv\Scripts\activate.bat
```

On **Linux/Mac**:
```bash
source venv/bin/activate
```

After activation, you should see `(venv)` at the beginning of your command prompt.

**To deactivate later:**
```bash
deactivate
```

### Step 1: Install Dependencies

Open your terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install Django and all required packages.

### Step 2: Run Database Migrations

Create the database tables by running:

```bash
python manage.py makemigrations
```

This creates migration files for your models. Then apply them:

```bash
python manage.py migrate
```

This creates all the necessary database tables (Quiz, Question, Choice, QuizSubmission, Answer, etc.).

**Expected Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, quiz_app, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying quiz_app.0001_initial... OK
```

### Step 3: Create a Superuser (Admin Account)

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username (e.g., `admin`)
- Email address (optional, press Enter to skip)
- Password (enter twice)

**Example:**
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

### Step 4: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 5: Access the Application

Open your web browser and navigate to:

- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Creating Your First Quiz

### Option A: Using Django Admin (Recommended)

1. Go to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Click on **"Quizzes"** → **"Add Quiz"**
   - Enter a title (e.g., "Python Basics Quiz")
   - Enter a description (optional)
   - Select yourself as "Created by"
   - Make sure "Is active" is checked
   - Click **"Save"**

4. Click on **"Questions"** → **"Add Question"**
   - Select your quiz
   - Enter question text (e.g., "What is Python?")
   - Select question type (Multiple Choice or Text)
   - Set order (0 for first question, 1 for second, etc.)
   - Click **"Save"**

5. For multiple choice questions, click on **"Choices"** → **"Add Choice"**
   - Select the question
   - Enter choice text (e.g., "A programming language")
   - Check "Is correct" for the correct answer
   - Click **"Save"**
   - Repeat for all answer choices

### Option B: Using Django Shell

```bash
python manage.py shell
```

Then paste this code:

```python
from django.contrib.auth.models import User
from quiz_app.models import Quiz, Question, Choice

# Get your admin user
user = User.objects.get(username='admin')  # Replace with your username

# Create a quiz
quiz = Quiz.objects.create(
    title='Sample Python Quiz',
    description='Test your Python knowledge',
    created_by=user,
    is_active=True
)

# Create a multiple choice question
q1 = Question.objects.create(
    quiz=quiz,
    question_text='What is Python?',
    question_type='multiple_choice',
    order=0
)

# Add choices
Choice.objects.create(question=q1, choice_text='A snake', is_correct=False)
Choice.objects.create(question=q1, choice_text='A programming language', is_correct=True)
Choice.objects.create(question=q1, choice_text='A type of pie', is_correct=False)

# Create another question
q2 = Question.objects.create(
    quiz=quiz,
    question_text='What is Django?',
    question_type='multiple_choice',
    order=1
)

Choice.objects.create(question=q2, choice_text='A web framework', is_correct=True)
Choice.objects.create(question=q2, choice_text='A database', is_correct=False)
Choice.objects.create(question=q2, choice_text='A programming language', is_correct=False)

print("Quiz created successfully!")
exit()
```

## Testing the Application

1. **Register a new trainee account:**
   - Go to http://127.0.0.1:8000/register/
   - Fill in username and password
   - Click "Register"

2. **Login:**
   - Go to http://127.0.0.1:8000/login/
   - Enter your credentials
   - Click "Login"

3. **Take a quiz:**
   - You'll see available quizzes on the home page
   - Click "Start Quiz" on any quiz
   - Answer the questions (answers auto-save)
   - Click "Submit Quiz" when finished
   - View your results with score and correct/incorrect answers

## Common Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run on different port (if 8000 is busy)
python manage.py runserver 8001

# Access Django shell
python manage.py shell

# Collect static files (if needed)
python manage.py collectstatic
```

## Troubleshooting

### Issue: "django-admin not found" or "python: command not found"
**Solution:** Make sure Python is installed and added to your PATH. Try using `python3` instead of `python` on some systems.

### Issue: "No module named 'django'"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: "Port 8000 already in use"
**Solution:** Use a different port: `python manage.py runserver 8001`

### Issue: Database errors after model changes
**Solution:** 
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: "TemplateDoesNotExist" error
**Solution:** Make sure you're running the server from the project root directory (where `manage.py` is located).

## Next Steps

- Create more quizzes with different question types
- Add more questions to existing quizzes
- Test the auto-save functionality
- Review quiz results and scoring
- Customize the UI in the templates folder

Happy quizzing! 🎉

