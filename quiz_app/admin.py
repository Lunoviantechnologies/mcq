from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django.http import HttpResponse
from .models import Quiz, Question, Choice, QuizSubmission, Answer
from .excel_utils import export_quizzes_to_excel, create_excel_template, import_quizzes_from_excel


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    actions = ['export_selected_quizzes']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('download-template/', self.admin_site.admin_view(self.download_template), name='quiz_download_template'),
            path('upload-excel/', self.admin_site.admin_view(self.upload_excel_view), name='quiz_upload_excel'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_import_export'] = True
        return super().changelist_view(request, extra_context=extra_context)
    
    def download_template(self, request):
        """Download Excel template for bulk import"""
        wb = create_excel_template()
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="quiz_import_template.xlsx"'
        wb.save(response)
        return response
    
    def upload_excel_view(self, request):
        """Handle Excel file upload for bulk import"""
        if request.method == 'POST' and request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            
            # Check file extension
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                messages.error(request, 'Please upload a valid Excel file (.xlsx or .xls)')
                return redirect('admin:quiz_app_quiz_changelist')
            
            # Import quizzes
            result = import_quizzes_from_excel(excel_file, request.user)
            
            if result['success']:
                messages.success(
                    request,
                    f'Successfully imported {result["success_count"]} quiz(es) from Excel file!'
                )
            else:
                if result['errors']:
                    for error in result['errors']:
                        messages.error(request, error)
                if result['success_count'] > 0:
                    messages.warning(
                        request,
                        f'Partially imported {result["success_count"]} quiz(es). Please check errors above.'
                    )
                else:
                    messages.error(request, 'Failed to import quizzes. Please check the Excel file format.')
            
            return redirect('admin:quiz_app_quiz_changelist')
        
        # GET request - show upload form
        context = {
            **self.admin_site.each_context(request),
            'title': 'Upload Excel File',
            'opts': self.model._meta,
            'has_view_permission': self.has_view_permission(request),
        }
        return render(request, 'admin/quiz_app/quiz/upload_excel.html', context)
    
    def export_selected_quizzes(self, request, queryset):
        """Export selected quizzes to Excel"""
        if not queryset.exists():
            messages.warning(request, 'Please select at least one quiz to export.')
            return
        
        wb = export_quizzes_to_excel(queryset)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="quizzes_export_{queryset.count()}_quizzes.xlsx"'
        wb.save(response)
        return response
    
    export_selected_quizzes.short_description = "Export selected quizzes to Excel"


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
