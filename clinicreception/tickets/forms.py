from django import forms
from .models import AppointmentTickets

class AppointmentTicketsForm(forms.ModelForm):
    class Meta:
        model = AppointmentTickets
        fields = '__all__'
        labels = {
            'ticket_date': 'Дата талону',
            'ticket_time': 'Час талону',
            'doctor': 'Лікар',
            'examination_type': 'Тип процедури',
            'patient': 'Пацієнт',
            'status': 'Статус проведення процедури',
            'card_status': 'Статус карти',
        }

        widgets = {
            'ticket_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'ticket_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'examination_type': forms.Select(attrs={'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'card_status': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditAppointmentTicketsForm(forms.ModelForm):
    class Meta:
        model = AppointmentTickets
        fields = ['ticket_date', 'ticket_time']
        labels = {
            'ticket_date': 'Дата талону',
            'ticket_time': 'Час талону',
        }

        widgets = {
            'ticket_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'ticket_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class AppointmentTicketStatusForm(forms.ModelForm):
    class Meta:
        model = AppointmentTickets
        fields = ['status']
        labels = {
            'status': 'Статус проведення процедури',
        }
        widgets = {
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

