from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import Doctors

class DoctorForm(forms.ModelForm):
    doctor_login = forms.CharField(label="Логін лікаря", max_length=65,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}),
                                                          error_messages={'required': '*'})
    doctor_password = forms.CharField(label="Пароль лікаря", max_length=40,
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                      error_messages={'required': '*'})
    class Meta:
        model = Doctors
        fields = '__all__'
        labels = {
            'doctor_id': 'ID лікаря',
            'full_name': 'Повне ім\'я',
            'job_title': 'Посада',
            'specialization': 'Спеціалізація',
            'birth_date': 'Дата народження',
            'status': 'Статус',
        }
        widgets = {
            'doctor_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        error_messages = {
            'full_name': {
                'required': '*',
            },
            'job_title': {
                'required': '*',
            },
            'specialization': {
                'required': '*',
            },
            'birth_date': {
                'required': '*',
                'invalid': 'Дата народження не може бути меншою за 25 років від поточної дати.',
            },
            'status': {
                'required': '*',
            },
        }



class DoctorFilterForm(forms.Form):
    status = forms.ChoiceField(choices=[(True, 'Працює'), (False, 'Не працює')],
                               widget=forms.Select(attrs={'class': 'form-control'}),
                               label='Статус',  error_messages={'required': '*'})

# doctors/forms.py


class DismissDoctorForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.filter(status=True), label="Виберіть лікаря для звільнення")


class SelectDoctorForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), label="Виберіть лікаря для редагування")


class EditDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ['full_name', 'job_title', 'specialization', 'birth_date']
        labels = {
            'full_name': 'Повне ім\'я',
            'job_title': 'Посада',
            'specialization': 'Спеціалізація',
            'birth_date': 'Дата народження',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }
        error_messages = {
                'full_name': {
                    'required': '*',
                },
                'job_title': {
                    'required': '*',
                },
                'specialization': {
                    'required': '*',
                },
                'birth_date': {
                    'required': '*',
                    'invalid': 'Дата народження не може бути меншою за 25 років від поточної дати.',
                },
        }

class PatientVisitsForm(forms.Form):
    start_date = forms.DateField(label='Дата початку', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Дата кінця', widget=forms.DateInput(attrs={'type': 'date'}))
    doctor_id = forms.IntegerField(label='ID лікаря', required=False)
