from __future__ import unicode_literals

import string
import random

from django.db import models
from django.contrib.auth.models import User

#Model for the doctor
class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email_subject = models.CharField(
        max_length=256,
        default="Wish you a very Happy and a Healthy birthday from Dr. {0}"
    )
    email_body = models.TextField(
        default=(
            "Dear [first name] [last name],\n\nHappy "
            "birthday!\n\nSincerely,\nDr. {0}"
        )
    )

    def __str__(self):
        return self.last_name
    #sets a random password for the doctor who has authorized to use this application 
    def set_random_password(self):
        user = self.user
        all_chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join((random.choice(all_chars)) for x in range(20))
        user.set_password(password)
        user.save()
        return password


#Model for the Patient
class Patient(models.Model):
    doctor = models.ForeignKey(Doctor)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    birthday = models.DateTimeField()
    send_email = models.BooleanField(default=False)
    #defines the ordering that we would be using while displaying patients
    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.email
