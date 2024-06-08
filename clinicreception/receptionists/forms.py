from django import forms
from .models import Receptionists


class ReceptionistForm(forms.ModelForm):
    receptionist_login = forms.CharField(label="Логін працівника", max_length=65,
                                         widget=forms.TextInput(attrs={'class': 'form-control'}),
                                         error_messages={'required': '*'})
    receptionist_password = forms.CharField(label="Пароль працівника", max_length=40,
                                            widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                            error_messages={'required': '*'})

    class Meta:
        model = Receptionists
        fields = '__all__'
        labels = {
            'receptionist_id': 'ID працівника',
            'full_name': 'Повне ім\'я',
            'job_title': 'Посада',
            'birth_date': 'Дата народження',
            'status': 'Статус',
        }
        widgets = {
            'receptionist_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.Select(attrs={'class': 'form-control'}),
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
            'birth_date': {
                'required': '*',
                'invalid': 'Дата народження не може бути меншою за 21 рік від поточної дати.',
            },
            'status': {
                'required': '*',
            },
        }
class ReceptionistFilterForm(forms.Form):
    status = forms.ChoiceField(choices=[('True', 'Активний'), ('False', 'Неактивний')], required=False, label='Статус')


class DismissReceptionistForm(forms.Form):
    receptionist = forms.ModelChoiceField(queryset=Receptionists.objects.all().filter(status=True), label="Працівник",
                                          widget=forms.Select(attrs={'class': 'form-control'}))