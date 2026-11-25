from django.urls import path
from . import views
from .views import deployment_django

app_name = 'course_app'

urlpatterns = [
    path('', views.course_list_view, name='course_list'),
    path('add/', views.course_create_view, name='course_create'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('<int:pk>/enroll/', views.course_enroll_view, name='course_enroll'),
    path('<int:pk>/', views.course_detail_view, name='course_detail'),
    path('<int:pk>/delete/', views.course_delete_view, name='course_delete'),
    path('management/', views.management_dashboard_view, name='management_dashboard'),
    path('management/courses/', views.management_courses_view, name='management_courses'),
    path('management/categories/',views.management_categories_view,name='management_categories'),
    path('<int:pk>/edit/', views.course_update_view, name='course_update'),
    path('management/students/',views.management_students_view,name='management_students'),
    path('', deployment_django, name='deployment'),

]

