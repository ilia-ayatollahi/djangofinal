from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class CourseCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='نام دسته‌بندی'
    )

    description = models.TextField(
        blank=True,
        verbose_name='توضیحات'
    )

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='دسته‌بندی'
    )

    #Level
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('comprehensive', 'Comprehensive'),
    ]


    #title
    title = models.CharField(max_length=100)

    #course description
    description = models.TextField()

    image = models.ImageField(
        upload_to='courses/',
        blank=True,
        null=True
    )

    #course rate
    rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    #teacher
    teacher = models.CharField(max_length=70)

    #price
    price = models.PositiveIntegerField()

    #duration
    duration = models.PositiveIntegerField()


    level = models.CharField(max_length= 20, choices=LEVEL_CHOICES, default='beginner')

    #certificate
    certificate = models.BooleanField(default=False)

    #prerequisites
    prerequisites = models.TextField()

    # maximum capacity
    capacity = models.PositiveIntegerField()

    # number of enrolled students
    enrolled_count = models.PositiveIntegerField(default=0)

    # enrolled students
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_courses',
        blank=True
    )

    # start date
    start_date = models.DateField()

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        if (
            self.capacity is not None
            and self.enrolled_count is not None
            and self.enrolled_count > self.capacity
        ):
            raise ValidationError('enrolled count cannot exceed capacity!')

    @property
    def students_count(self):
        return self.students.count()

    @property
    def remaining_capacity(self):
        return max(0, self.capacity - self.students_count)

    @property
    def is_full(self):
        return self.students_count >= self.capacity


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone_number = models.CharField(max_length=15)

    birth_date = models.DateField(
        null=True,
        blank=True
    )

    national_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        unique=True
    )

    father_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    address = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username