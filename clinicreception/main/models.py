# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AppointmentTickets(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey('Doctors', models.DO_NOTHING, db_column='doctor')
    examination_type = models.ForeignKey('Skills', models.DO_NOTHING, db_column='examination_type')
    patient = models.ForeignKey('MedicalCards', models.DO_NOTHING, db_column='patient')
    ticket_date = models.DateField()
    ticket_time = models.TimeField()
    status = models.BooleanField()
    card_status = models.CharField(max_length=40, default='У реєстратурі')

    def __str__(self):
        return self.card_status

    class Meta:
        managed = False
        db_table = 'appointment_tickets'
        verbose_name = 'Талон'
        verbose_name_plural = 'Талони'
        ordering = ["ticket_date", 'ticket_id']


class Doctors(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=60)
    job_title = models.CharField(max_length=60, choices=[
         ('Головний лікар', 'Головний лікар'),
            ('Завідувач відділення', 'Завідувач відділення'),
            ('Старший лікар', 'Старший лікар'),
            ('Лікар', 'Лікар'),
            ('Лікар-ординатор', 'Лікар-ординатор'),
            ('Лікар-стажер', 'Лікар-стажер'),
            ('Фельдшер', 'Фельдшер'),
            ('Медсестра', 'Медсестра'),
            ('Медбрат', 'Медбрат'),
            ('Молодша медсестра', 'Молодша медсестра'),
            ('Молодший медбрат', 'Молодший медбрат'),
        ])
    specialization = models.ForeignKey('Specializations', models.DO_NOTHING, db_column='specialization')
    birth_date = models.DateField()
    status = models.BooleanField()


    def __str__(self):
        return self.full_name

    class Meta:
        managed = False
        db_table = 'doctors'
        ordering = ['full_name']


class Examinations(models.Model):
    examination_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctors, models.DO_NOTHING, db_column='doctor')
    skills = models.ForeignKey('Skills', models.DO_NOTHING, db_column='skills')

    class Meta:
        managed = False
        db_table = 'examinations'
        unique_together = (('doctor', 'skills'),)


class MedicalCards(models.Model):
    SEX_CHOICES = [
        ('ж', 'Жіночий'),
        ('ч', 'Чоловічий'),
    ]

    medcard_id = models.AutoField(primary_key=True)
    patient_fullname = models.CharField(max_length=60)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birth_date = models.DateField()
    address = models.CharField(max_length=200)
    workplace_position = models.TextField(blank=True, null=True)
    patient_privileges = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=15, validators=[
            RegexValidator(
                regex=r'\(0[0-9]{2}\)\-[0-9]{3}\-[0-9]{2}\-[0-9]{2}',
                message='Номер телефону повинен бути у форматі: (0XX)-XXX-XX-XX.'
            )
        ], blank=True, null=True)
    status = models.CharField(max_length=40, default='У реєстратурі')

    def __str__(self):
        return self.patient_fullname

    class Meta:
        managed = False
        db_table = 'medical_cards'
        ordering = ['medcard_id', 'patient_fullname']


class Receptionists(models.Model):
    JOB_TITLE_CHOICES = [
        ('Медичний реєстратор', 'Медичний реєстратор'),
        ('Контролер медичних карт', 'Контролер медичних карт'),
        ('Адміністратор', 'Адміністратор'),
        ('Аналітик статистики пацієнтів', 'Аналітик статистики пацієнтів'),
        ('Завідуючий реєстратурою', 'Завідуючий реєстратурою'),
    ]

    receptionist_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=60)
    job_title = models.CharField(max_length=60, choices=JOB_TITLE_CHOICES)
    birth_date = models.DateField()
    status = models.BooleanField()


    def __str__(self):
        return self. full_name

    class Meta:
        managed = False
        db_table = 'receptionists'
        ordering = ['full_name']


class Schedules(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    day_for_visits = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    cabinet = models.SmallIntegerField()
    doctor = models.ForeignKey(Doctors, models.DO_NOTHING, db_column='doctor')

    def __str__(self):
        return self.doctor

    class Meta:
        managed = False
        db_table = 'schedules'
        ordering = ['doctor']


class Skills(models.Model):
    skill_id = models.AutoField(primary_key=True)
    specialization = models.ForeignKey('Specializations', models.DO_NOTHING, db_column='specialization')
    examination_type = models.TextField()

    def __str__(self):
        return self.examination_type

    class Meta:
        managed = False
        db_table = 'skills'


class Specializations(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    specialization = models.CharField(max_length=70)

    def __str__(self):
        return self.specialization

    class Meta:
        managed = False
        db_table = 'specializations'


