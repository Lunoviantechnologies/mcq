# Django Quiz Application

A Google Forms-like quiz application built with Django, allowing trainees to log in and take quizzes.

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

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**:
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Trainees:

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

### For Administrators:

1. **Access Admin Panel**: Log in at `/admin/`
2. **Create Quizzes**: 
   - Go to "Quizzes" section
   - Click "Add Quiz"
   - Enter title and description
3. **Add Questions**:
   - Go to "Questions" section
   - Click "Add Question"
   - Select quiz, enter question text, choose type
   - Set order number
4. **Add Choices** (for multiple choice):
   - Go to "Choices" section
   - Click "Add Choice"
   - Select question, enter choice text
   - Check "Is correct" for the correct answer

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
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Models

- **Quiz**: Represents a quiz with title, description, and creator
- **Question**: Questions within a quiz (multiple choice or text)
- **Choice**: Answer choices for multiple choice questions
- **QuizSubmission**: Tracks when a trainee starts/completes a quiz
- **Answer**: Stores individual answers to questions

## Security Features

- CSRF protection enabled
- User authentication required for quiz access
- Users can only view their own quiz results
- Password validation on registration

## Future Enhancements

- Timer functionality for quizzes
- Question randomization
- Multiple attempts allowed
- Export results to PDF
- Email notifications
- Quiz analytics dashboard

