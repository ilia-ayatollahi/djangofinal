from django.contrib import admin
from .models import Course

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'teacher',
        'level',
        'price',
        'duration',
        'students_count',
        'capacity',
        'start_date',
    ]
    search_fields = ['title', 'teacher', 'description']
    list_filter = ['level', 'certificate', 'start_date']
    list_editable = ['price', 'capacity']
    list_per_page = 20

    ordering = ('-date_created',)



