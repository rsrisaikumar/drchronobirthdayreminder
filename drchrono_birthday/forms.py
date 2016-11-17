from django import forms

from .models import Doctor, Patient


#Fields that are to be updated on email edit
class EmailForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['email_subject', 'email_body']


#field that is to be updated on decision to send/cancel greeting
class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['send_email']
