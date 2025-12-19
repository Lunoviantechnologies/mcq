# Django Quiz Application

A Google Forms-like quiz application built with Django, allowing trainees to register, log in, and take quizzes with multiple question types.

## Features

- **User Authentication**: Registration and login system for trainees
- **Quiz Management**: Create and manage quizzes with multiple question types
- **Question Types**: 
  - Multiple choice questions
  - Text-based questions
- **Auto-save**: Answers are automatically saved as you progress
- **Progress Tracking**: Visual progress bar showing completion status
- **Results View**: Detailed results page showing scores and correct/incorrect answers
- **Modern UI**: Beautiful, responsive interface with gradient backgrounds

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Quick Start

### Step 1: Clone and Navigate to Project

```bash
cd path/to/project
```

### Step 2: Create Virtual Environment (Recommended)

**Create virtual environment:**
```bash
python -m venv venv
```

**Activate virtual environment:**

- **Windows (PowerShell):**
  ```bash
  .\venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt):**
  ```bash
  venv\Scripts\activate.bat
  ```

- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

You should see `(venv)` at the beginning of your command prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration (Optional)

For production or custom database configuration, copy `.env.example` to `.env` and update the values:

```bash
# On Linux/Mac
cp .env.example .env

# On Windows
copy .env.example .env
```

Edit `.env` with your configuration (database credentials, secret key, etc.).

### Step 5: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 7: Run Development Server

```bash
python manage.py runserver
```

The application will be available at:
- **Main application**: http://127.0.0.1:8000/
- **Admin panel**: http://127.0.0.1:8000/admin/

## Usage

### For Trainees

1. **Register**: Create a new account at `/register/`
2. **Login**: Log in at `/login/`
3. **View Quizzes**: See all available quizzes on the home page
4. **Start Quiz**: Click "Start Quiz" on any available quiz
5. **Answer Questions**: 
   - Select answers for multiple choice questions
   - Type answers for text questions
   - Answers are auto-saved as you progress
6. **Submit**: Click "Submit Quiz" when finished
7. **View Results**: See your score and review answers

### For Administrators

1. **Access Admin Panel**: Log in at `/admin/`
2. **Create Quizzes**: 
   - Go to "Quizzes" section
   - Click "Add Quiz"
   - Enter title and description
   - Select yourself as "Created by"
   - Check "Is active" to make it available
3. **Add Questions**:
   - Go to "Questions" section
   - Click "Add Question"
   - Select quiz, enter question text, choose type
   - Set order number (0 for first question, 1 for second, etc.)
4. **Add Choices** (for multiple choice):
   - Go to "Choices" section
   - Click "Add Choice"
   - Select question, enter choice text
   - Check "Is correct" for the correct answer
   - Repeat for all choices

### Creating Sample Data

You can create sample data using Django Admin or Django Shell:

**Using Django Shell:**
```bash
python manage.py shell
```

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

# Create choices
Choice.objects.create(question=q1, choice_text='A snake', is_correct=False)
Choice.objects.create(question=q1, choice_text='A programming language', is_correct=True)
Choice.objects.create(question=q1, choice_text='A type of pie', is_correct=False)

print("Sample quiz created successfully!")
exit()
```

## Project Structure

```
quiz_project/
├── quiz_project/          # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── quiz_app/              # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL configuration
│   ├── admin.py           # Admin configuration
│   └── templatetags/      # Custom template filters
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── quiz_app/          # App-specific templates
├── static/                # Static files (CSS, JS, images)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables example
└── README.md              # This file
```

## Database Models

- **Quiz**: Represents a quiz with title, description, and creator
- **Question**: Questions within a quiz (multiple choice or text)
- **Choice**: Answer choices for multiple choice questions
- **QuizSubmission**: Tracks when a trainee starts/completes a quiz
- **Answer**: Stores individual answers to questions

## URL Routes

- `/` - Quiz list (login required)
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/quiz/<id>/start/` - Start a quiz
- `/quiz/<id>/` - Take a quiz
- `/quiz/<id>/submit-answer/` - Auto-save answer (AJAX)
- `/quiz/<id>/submit/` - Submit completed quiz
- `/results/<submission_id>/` - View quiz results

## Security Features

- CSRF protection enabled
- Password validation on registration
- User authentication required for quiz access
- Users can only view their own quiz results
- SQL injection protection (Django ORM)
- XSS protection (Django template auto-escaping)

## Technologies Used

- **Backend**: Django 4.2+
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)

## Common Commands

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

# Collect static files (production)
python manage.py collectstatic

# Access Django shell
python manage.py shell
```

## Troubleshooting

### Issue: "No module named 'django'"
**Solution:** Make sure the virtual environment is activated and install dependencies: `pip install -r requirements.txt`

### Issue: "Port 8000 already in use"
**Solution:** Use a different port: `python manage.py runserver 8001`

### Issue: "Database errors after model changes"
**Solution:** 
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Activate.ps1 cannot be loaded" (Windows PowerShell)
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Static files not loading
**Solution:**
```bash
python manage.py collectstatic
```

## Deployment

For deployment instructions on AWS EC2 with RDS MySQL, see `DEPLOY_AWS_EC2_RDS_MYSQL.md`.

## Future Enhancements

- Timer functionality for quizzes
- Question randomization
- Multiple attempts allowed
- Export results to PDF/CSV
- Email notifications
- Quiz analytics dashboard
- Image support in questions
- Drag-and-drop question ordering
- Quiz categories/tags
- Bulk question import

## License

This project is open source and available for use.
