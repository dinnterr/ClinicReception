from django import forms
from django.core.validators import MinValueValidator

from .models import Schedules, Doctors


class DoctorSelectForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), label='Оберіть лікаря', widget=forms.Select(attrs={'class': 'form-control'}))

class ScheduleCreateForm(forms.ModelForm):
    class Meta:
        model = Schedules
        fields = ['day_for_visits', 'start_time', 'end_time', 'cabinet', 'doctor']
        widgets = {
            'day_for_visits': forms.Select(
                choices=[('Понеділок', 'Понеділок'), ('Вівторок', 'Вівторок'), ('Середа', 'Середа'),
                         ('Четвер', 'Четвер'), ('П`ятниця', 'П`ятниця'), ('Субота', 'Субота'), ('Неділя', 'Неділя')],
                attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cabinet': forms.NumberInput(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'day_for_visits': 'День відвідувань',
            'start_time': 'Час початку',
            'end_time': 'Час закінчення',
            'cabinet': 'Кабінет',
            'doctor': 'Лікар',
        }

class ScheduleUpdateForm(forms.ModelForm):
    class Meta:
        model = Schedules
        fields = ['day_for_visits', 'start_time', 'end_time', 'cabinet']

        widgets = {
            'day_for_visits': forms.Select(
                choices=[('Понеділок', 'Понеділок'), ('Вівторок', 'Вівторок'), ('Середа', 'Середа'),
                         ('Четвер', 'Четвер'), ('П`ятниця', 'П`ятниця'), ('Субота', 'Субота'), ('Неділя', 'Неділя')],
                attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cabinet': forms.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
                'day_for_visits': 'День відвідувань',
                'start_time': 'Час початку',
                'end_time': 'Час закінчення',
                'cabinet': 'Кабінет'
            }
