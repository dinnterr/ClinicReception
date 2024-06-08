from django import forms
from django.core.validators import MinValueValidator

from .models import MedicalCards

class MedicalCardsForm(forms.ModelForm):
    class Meta:
        model = MedicalCards
        fields = '__all__'
        labels = {
            'medcard_id': 'ID медичної картки',
            'patient_fullname': 'Повне ім\'я пацієнта',
            'sex': 'Стать',
            'birth_date': 'Дата народження',
            'address': 'Адреса',
            'workplace_position': 'Посада на роботі',
            'patient_privileges': 'Привілеї пацієнта',
            'status': 'Статус (місцезнаходження карти)',
            'phone_number': 'Номер телефону',
        }
        widgets = {
            'medcard_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'patient_fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'workplace_position': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'patient_privileges': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': '(0XX)-XXX-XX-XX',
                    'oninput': 'formatPhoneNumber(this)',
                }),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'patient_fullname': {
                'required': '*',
            },
            'sex': {
                'required': '*',
            },
            'birth_date': {
                'required': '*',
                'invalid': 'Дата народження не може бути в майбутньому.',
            },
            'address': {
                'required': '*',
            },
            'phone_number': {
                'invalid': 'Номер телефону повинен бути у форматі: (0XX)-XXX-XX-XX.',
            },
            'status': {
                'required': '*',
            },
        }


class MedicalCardSearchForm(forms.Form):
    medcard_id = forms.IntegerField(
        label='№ медичної картки',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        validators=[MinValueValidator(1)],  # Добавляем валидатор
        error_messages={'required': '*', 'min_value': 'Номер медичної картки повинен бути більше нуля.'}
    )

class MedicalCardSearchSt(forms.Form):
    medcard_id = forms.IntegerField(
        label='№ медичної картки',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        validators=[MinValueValidator(1)],  # Добавляем валидатор
        error_messages={'required': '*', 'min_value': 'Номер медичної картки повинен бути більше нуля.'},
    )

class DeliveryForm(forms.Form):
    ticket_id = forms.IntegerField(
        label='Номер талону',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    new_status = forms.CharField(
        label='Новий статус місцезнаходження медичної карти',
        max_length=40,
        initial='У лікаря',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class RemoveForm(forms.Form):
    medcard_id = forms.IntegerField(
        label='Номер медичної карти',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    new_status = forms.CharField(
        label='Новий статус місцезнаходження медичної карти',
        max_length=40,
        initial='Вилучено',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class ArchiveForm(forms.Form):
    medcard_id = forms.IntegerField(
        label='Номер медичної карти',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    new_status = forms.CharField(
        label='Новий статус місцезнаходження медичної карти',
        max_length=40,
        initial='Архівовано',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class AgeAppointmentForm(forms.Form):
    medcard_ids = forms.CharField(
        label='№ медичних карток (через кому)',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )