# Excel Import/Export Guide for Quiz Admin

This guide explains how to use the Excel import/export functionality in the Django Admin panel.

## Features

1. **Download Excel Template** - Get a pre-formatted template with instructions
2. **Export Quizzes** - Export selected quizzes with all questions and choices to Excel
3. **Bulk Import** - Upload Excel file to create multiple quizzes, questions, and choices at once

## How to Use

### Export Quizzes to Excel

1. Go to **Admin Panel** → **Quizzes**
2. Select the quizzes you want to export (checkboxes)
3. From the **Action** dropdown, select **"Export selected quizzes to Excel"**
4. Click **"Go"**
5. Excel file will be downloaded with three sheets:
   - **Quizzes** - Quiz information
   - **Questions** - All questions for selected quizzes
   - **Choices** - All choices for multiple choice questions

### Download Template for Import

1. Go to **Admin Panel** → **Quizzes**
2. Click **"📥 Download Excel Template"** button (top right)
3. Excel file will be downloaded with:
   - **Instructions** sheet - Detailed instructions on how to fill the template
   - **Quizzes** sheet - Template for quiz data
   - **Questions** sheet - Template for question data
   - **Choices** sheet - Template for choice data (with examples)

### Bulk Import Quizzes from Excel

1. **Download the template** first (see above)
2. **Fill in your data**:
   - Add quizzes in the **Quizzes** sheet
   - Add questions in the **Questions** sheet
   - Add choices in the **Choices** sheet (only for Multiple Choice questions)
3. Go to **Admin Panel** → **Quizzes**
4. Click **"📤 Upload Excel File"** button (top right)
5. Select your filled Excel file
6. Click **"Upload and Import"**
7. Check the messages for import results/errors

## Excel File Format

### Quizzes Sheet

| Quiz Title | Description | Created By | Is Active |
|------------|-------------|------------|-----------|
| Sample Quiz | This is a sample quiz | admin | Yes |

**Required:**
- Quiz Title (must be unique, used as identifier)

**Optional:**
- Description
- Created By (username, defaults to current user if not found)
- Is Active (Yes/No, defaults to Yes)

### Questions Sheet

| Quiz Title | Question Text | Question Type | Order | Time Limit (minutes) |
|------------|---------------|---------------|-------|---------------------|
| Sample Quiz | What is Python? | Multiple Choice | 0 | 1 |
| Sample Quiz | Explain Python | Text Answer | 1 | 2 |

**Required:**
- Quiz Title (must match exactly with Quiz Title in Quizzes sheet)
- Question Text

**Optional:**
- Question Type: "Multiple Choice" or "Text Answer" (defaults to "Multiple Choice")
- Order: Number (0, 1, 2, ...) - defaults to 0
- Time Limit: Minutes allowed (defaults to 1)

### Choices Sheet (Only for Multiple Choice Questions)

| Quiz Title | Question Text | Choice Text | Is Correct |
|------------|---------------|-------------|------------|
| Sample Quiz | What is Python? | A snake | No |
| Sample Quiz | What is Python? | A programming language | Yes |
| Sample Quiz | What is Python? | A type of pie | No |

**Required:**
- Quiz Title (must match exactly)
- Question Text (must match exactly with Questions sheet)
- Choice Text

**Optional:**
- Is Correct: Yes/No (defaults to No)

**Important Notes:**
- Only Multiple Choice questions need choices
- At least one choice per question should have Is Correct = "Yes"
- Each Multiple Choice question should have at least 2 choices

## Best Practices

1. **Start with the template** - Always download the template first to ensure correct format
2. **Match exactly** - Quiz Titles must match exactly across all sheets (case-sensitive)
3. **Use unique titles** - Each quiz should have a unique title
4. **Check before import** - Review your Excel file before uploading
5. **Order numbers** - Use sequential order numbers (0, 1, 2, ...) for questions
6. **Validate data** - Ensure Multiple Choice questions have at least 2 choices with one correct answer

## Troubleshooting

### Import Errors

- **"Quiz not found"** - Quiz Title in Questions/Choices sheet doesn't match Quizzes sheet (check spelling/case)
- **"Question not found"** - Question Text in Choices sheet doesn't match Questions sheet
- **"User not found"** - Created By username doesn't exist (will use current user as fallback)
- **"Question text is required"** - Empty question text in Questions sheet

### Common Issues

1. **Duplicate quizzes** - If quiz title already exists, it will be updated (not duplicated)
2. **Missing choices** - Multiple Choice questions without choices won't work properly
3. **No correct answer** - Multiple Choice questions should have at least one choice with Is Correct = "Yes"

## Tips

- Export existing quizzes first to see the format
- Use the template's example rows as reference
- Test with a small dataset first (1-2 quizzes)
- Check error messages after import for specific issues
- Quiz Titles are case-sensitive and must match exactly

## Technical Details

- **Library Used**: `openpyxl` for Excel file handling
- **Supported Formats**: `.xlsx`, `.xls`
- **File Size Limit**: Depends on server configuration (typically 2-10MB)
- **Encoding**: UTF-8
- **Date Format**: Dates are stored as strings in Excel, converted by Django

