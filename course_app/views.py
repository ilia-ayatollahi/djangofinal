from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, UserProfile, CourseCategory
from .forms import NewCourseForm, RegisterForm, CourseCategoryForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.http import HttpResponse

def home_view(request):
    featured_courses = Course.objects.all().order_by('-date_created')[:3]

    total_courses = Course.objects.count()
    total_students = Course.students.through.objects.count()

    return render(
        request,
        'home.html',
        {
            'featured_courses': featured_courses,
            'total_courses': total_courses,
            'total_students': total_students,
        }
    )

# Create your views here.

# course list
def course_list_view(request):
    courses = Course.objects.all().order_by('-date_created')

    categories = CourseCategory.objects.all().order_by('name')

    selected_category = request.GET.get('category')

    if selected_category:
        courses = courses.filter(category_id=selected_category)

    return render(
        request,
        'course/course_list.html',
        {
            'courses': courses,
            'categories': categories,
            'selected_category': selected_category,
        }
    )

def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = course.students.filter(pk=request.user.pk).exists()

    return render(
        request,
        'course/course_detail.html',
        {
            'course': course,
            'is_enrolled': is_enrolled,
        }
    )
@login_required
def course_enroll_view(request, pk):
    if request.method != 'POST':
        return redirect('course_app:course_detail', pk=pk)

    with transaction.atomic():
        course = get_object_or_404(
            Course.objects.select_for_update(),
            pk=pk
        )

        if course.students.filter(pk=request.user.pk).exists():
            return redirect('course_app:course_detail', pk=pk)

        if course.is_full:
            return redirect('course_app:course_detail', pk=pk)

        course.students.add(request.user)

    return redirect('course_app:course_detail', pk=pk)

@staff_member_required
def course_create_view(request):
    if request.method == 'POST':
        form = NewCourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_app:course_list')
    else:
        form = NewCourseForm()
    return render(request, 'course/course_form.html', {'form': form})

@staff_member_required
def management_courses_view(request):
    courses = Course.objects.all().order_by('-date_created')

    categories = CourseCategory.objects.all().order_by('name')

    search_query = request.GET.get('search', '').strip()
    teacher_query = request.GET.get('teacher', '').strip()
    selected_category = request.GET.get('category', '').strip()

    if search_query:
        courses = courses.filter(title__icontains=search_query)

    if teacher_query:
        courses = courses.filter(teacher__icontains=teacher_query)

    if selected_category:
        courses = courses.filter(category_id=selected_category)

    return render(
        request,
        'management/courses.html',
        {
            'courses': courses,
            'categories': categories,
            'search_query': search_query,
            'teacher_query': teacher_query,
            'selected_category': selected_category,
        }
    )

@staff_member_required
def management_categories_view(request):
    if request.method == 'POST':
        form = CourseCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('course_app:management_categories')
    else:
        form = CourseCategoryForm()

    categories = CourseCategory.objects.all().order_by('name')

    return render(
        request,
        'management/categories.html',
        {
            'form': form,
            'categories': categories,
        }
    )

@staff_member_required
def management_students_view(request):
    students = (
        User.objects
        .filter(enrolled_courses__isnull=False)
        .distinct()
        .prefetch_related('enrolled_courses')
        .select_related('profile')
        .order_by('username')
    )

    return render(
        request,
        'management/students.html',
        {'students': students}
    )

@staff_member_required
def course_update_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = NewCourseForm(
            request.POST,
            request.FILES,
            instance=course
        )
        if form.is_valid():
            form.save()
            return redirect('course_app:management_courses')
    else:
        form = NewCourseForm(instance=course)

    return render(
        request,
        'management/course_form.html',
        {'form': form, 'course': course}
    )

@staff_member_required
def course_delete_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        course.delete()
        return redirect('course_app:course_list')

    return render(
        request,
        'course/course_confirm_delete.html',
        {'course': course}
    )

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def student_dashboard_view(request):
    enrolled_courses = request.user.enrolled_courses.all().order_by('-date_created')

    return render(
        request,
        'course/student_dashboard.html',
        {'enrolled_courses': enrolled_courses}
    )

@staff_member_required
def management_dashboard_view(request):

    total_courses = Course.objects.count()

    total_categories = CourseCategory.objects.count()

    total_enrollments = Course.students.through.objects.count()

    total_students = (
        Course.students.through.objects
        .values('user_id')
        .distinct()
        .count()
    )

    total_capacity = sum(
        Course.objects.values_list('capacity', flat=True)
    )

    available_seats = max(0, total_capacity - total_enrollments)

    latest_courses = Course.objects.order_by('-date_created')[:5]

    context = {
        'total_courses': total_courses,
        'total_categories': total_categories,
        'total_students': total_students,
        'total_enrollments': total_enrollments,
        'available_seats': available_seats,
        'latest_courses': latest_courses,
    }

    return render(request, 'management/dashboard.html', context)

def deployment_django(request):
    return HttpResponse("Deployment Django")