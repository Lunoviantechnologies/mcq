# Virtual Environment Setup Guide

## Project Location
**Project Directory:** `C:\Users\yash\Desktop\HR`

The Django quiz project is located in the `HR` folder on your Desktop. All project files (manage.py, quiz_app/, quiz_project/, etc.) are in this directory.

## Why Use a Virtual Environment?

A virtual environment (venv) isolates your project's dependencies from other Python projects on your system. This prevents conflicts between different projects that might use different versions of the same package.

## Creating a Virtual Environment

### Step 1: Navigate to Project Directory

Open your terminal/command prompt and navigate to the project directory:

```bash
cd C:\Users\yash\Desktop\HR
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

This creates a `venv` folder in your project directory.

### Step 3: Activate Virtual Environment

**On Windows PowerShell:**
```bash
.\venv\Scripts\Activate.ps1
```

**On Windows Command Prompt (CMD):**
```bash
venv\Scripts\activate.bat
```

**On Linux/Mac:**
```bash
source venv/bin/activate
```

**Success indicator:** You should see `(venv)` at the start of your command prompt:
```
(venv) PS C:\Users\yash\Desktop\HR>
```

### Step 4: Install Dependencies

With the virtual environment activated, install Django and other dependencies:

```bash
pip install -r requirements.txt
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Run the Server

```bash
python manage.py runserver
```

## Deactivating Virtual Environment

When you're done working on the project, deactivate the virtual environment:

```bash
deactivate
```

## Important Notes

1. **Always activate the virtual environment** before working on the project
2. The `venv` folder is already added to `.gitignore`, so it won't be committed to git
3. If you delete the `venv` folder, you'll need to recreate it and reinstall dependencies
4. Each project should have its own virtual environment

## Troubleshooting

### Issue: "Activate.ps1 cannot be loaded because running scripts is disabled"

**Solution for PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```bash
.\venv\Scripts\Activate.ps1
```

### Issue: "python: command not found"

**Solution:** 
- Make sure Python is installed
- Try using `python3` instead of `python`
- On Windows, you might need to add Python to your PATH

### Issue: "No module named 'django'"

**Solution:** 
- Make sure the virtual environment is activated (you should see `(venv)` in your prompt)
- Run `pip install -r requirements.txt` again

## Complete Setup Sequence

Here's the complete sequence of commands to set up the project from scratch:

```bash
# 1. Navigate to project directory
cd C:\Users\yash\Desktop\HR

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create migrations
python manage.py makemigrations

# 6. Apply migrations
python manage.py migrate

# 7. Create superuser (optional)
python manage.py createsuperuser

# 8. Run the server
python manage.py runserver
```

## Project Structure

```
C:\Users\yash\Desktop\HR\
├── venv\                    # Virtual environment (created)
├── quiz_project\            # Django project settings
├── quiz_app\                # Main quiz application
├── templates\               # HTML templates
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── db.sqlite3               # Database (created after migrate)
└── ... (other files)
```

