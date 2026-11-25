from django import forms
from django.forms import ModelForm
from .models import Course, UserProfile, CourseCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class NewCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'category',
            'description',
            'image',
            'rate',
            'teacher',
            'price',
            'duration',
            'level',
            'certificate',
            'prerequisites',
            'capacity',
            'start_date',
        ]

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'certificate':
                continue
            field.widget.attrs['class'] = 'input select' if name == 'level' else 'input'


class CourseCategoryForm(ModelForm):
    class Meta:
        model = CourseCategory
        fields = ['name', 'description']

        labels = {
            'name': 'نام دسته‌بندی',
            'description': 'توضیحات',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'مثلاً برنامه‌نویسی'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'توضیح کوتاهی درباره دسته‌بندی'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'
            

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='ایمیل'
    )

    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label='شماره تلفن همراه',
        widget=forms.TextInput(attrs={
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
            'placeholder': 'شماره تلفن همراه را وارد کنید'
        })
    )

    birth_date = forms.DateField(
        required=True,
        label='تاریخ تولد',
        widget=forms.DateInput(attrs={
            'type': 'date'
        })
    )

    national_code = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        label='کد ملی'
    )

    father_name = forms.CharField(
        max_length=100,
        required=True,
        label='نام پدر'
    )

    city = forms.CharField(
        max_length=100,
        required=True,
        label='شهر محل سکونت'
    )

    address = forms.CharField(
        required=True,
        label='آدرس محل سکونت',
        widget=forms.Textarea(attrs={
            'rows': 3
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'birth_date',
            'national_code',
            'father_name',
            'city',
            'address',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full rounded-xl px-4 py-3',
                'style': 'border: 1px solid #d1d5db; background: white;'
            })

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                birth_date=self.cleaned_data['birth_date'],
                national_code=self.cleaned_data['national_code'],
                father_name=self.cleaned_data['father_name'],
                city=self.cleaned_data['city'],
                address=self.cleaned_data['address']
            )

        return user

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']

        if not phone.isdigit():
            raise forms.ValidationError(
                'شماره تلفن فقط باید شامل اعداد باشد.'
            )

        return phone

    def clean_national_code(self):
        code = self.cleaned_data['national_code']

        if not code.isdigit():
            raise forms.ValidationError(
                'کد ملی فقط باید شامل اعداد باشد.'
            )

        if UserProfile.objects.filter(national_code=code).exists():
            raise forms.ValidationError(
                'این کد ملی قبلاً ثبت شده است.'
            )

        return code
