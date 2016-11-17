from django.core.management.base import BaseCommand
from drchrono_birthday.models import Doctor
from django.core.mail import send_mass_mail

import datetime

from drchrono_wishes.settings import EMAIL_HOST_USER

#send mass emails through django's in-built send_mass_mail service

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

	#extract patients that doctor wishes to greet
        def get_bday_emails(doctor):
            emails = []
            patients = doctor.patient_set.filter(send_email=True)
            for patient in patients:
                if is_birthday(patient):
                    message = (generate_email(doctor, patient))
                    emails.append(message)

            return emails

	#checks if it is the patient's birthday
        def is_birthday(patient):
            currentDate = datetime.date.today()
            birthday = patient.birthday
            if (birthday.month == currentDate.month and
                    birthday.day == currentDate.day):
                return True

            return False

	#generate the message by extracting patient's details
        def generate_email(doctor, patient):
            subject = doctor.email_subject.format(doctor.last_name)
            subject = subject.replace(
                '[first name]', patient.first_name
            ).replace(
                '[last name]', patient.last_name
            )

            body = doctor.email_body.format(doctor.last_name)
            body = body.replace(
                '[first name]', patient.first_name
            ).replace(
                '[last name]', patient.last_name
            )

            message = (subject, body, EMAIL_HOST_USER, [patient.email])
            return message

        doctors = Doctor.objects.all()
        emails = []
        for doctor in doctors:
            emails.extend(get_bday_emails(doctor))

        send_mass_mail(tuple(emails), fail_silently=False)
