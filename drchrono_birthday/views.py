from django.core import serializers
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import HttpResponse, QueryDict
from django.views import generic
from django.db.models import *
from django.utils.http import urlquote
from .models import Doctor, Patient
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import EmailForm, PatientForm
from drchrono_wishes.settings import CLIENT_DATA
from .utils import *


#renders index.html
def index(request):	
	return render(request, 'index.html', context={
        'redirect_url': urlquote(CLIENT_DATA['redirect_url']),
        'client_id': CLIENT_DATA['client_id']
    })


#redirects here when user clicks guest login
def guest(request):
	auth_user = authenticate(username="guest", password="password")
	login(request, auth_user)
	return redirect('drchrono_birthday:home')


#renders home.html to display user's home page
def home(request):
	if request.user.is_authenticated()==False:
		return redirect('drchrono_birthday:error')
	doctor = request.user.doctor
	patients = doctor.patient_set.all()
	context={
		'doctor':doctor,
		'patients':patients
	}
	return render(request, 'home.html', context)	


#In case of any error
def error(request):
	return render(request, 'error.html')


#logout the user and redirect to index
def log_out(request):
    logout(request)
    return redirect('drchrono_birthday:index')


#render email.html with doctor's email details
def edit_email(request):
    user = request.user
    doctor = user.doctor
    context = {
        'user': user,
        'email_subject': doctor.email_subject.format(doctor.last_name),
        'email_body': doctor.email_body.format(doctor.last_name),
    }

    return render(request, 'email.html', context)


#Comes here on some query to search a patient
def patient_search(request):
    patients = request.user.doctor.patient_set.all()
    if request.method == 'GET' and request.GET['queryString']:
        query_string = request.GET['queryString']
        patients = patients.filter(
            Q(last_name__contains=query_string) |
            Q(first_name__contains=query_string) |
            Q(email__contains=query_string)
        )

    return render(request, 'patients.html', {
        'patients': patients
    })	


#Redirect destination for drchrono. Handles user login and updating db with
#new drchrono data.
def oauth(request):
    if 'error' in request.GET:
        return redirect('drchrono_birthday:error')

    user = get_drchrono_user(request.GET)
    auth_user = authenticate(
        username=user.username,
        password=user.doctor.set_random_password()
    )
    login(request, auth_user)
    return redirect('drchrono_birthday:home')


#new class to update the new email information for the doctor
class DoctorView(generic.DetailView):
    model = Doctor

    def patch(self, request, **kwargs):
        doctor = get_object_or_404(User, doctor=kwargs['pk']).doctor
        data = QueryDict(request.body)
        form = EmailForm(data, instance=doctor)
        if form.is_valid():
            form.save()
            doctorJSON = serializers.serialize("json", [doctor])
            return HttpResponse(doctorJSON, content_type='application/json')

        return HttpResponse(status=500)


#new class to update email receive by the patient
class PatientView(generic.DetailView):
    model = Patient

    def patch(self, request, **kwargs):
        patient = get_object_or_404(Patient, pk=kwargs['pk'])
        data = QueryDict(request.body)
        form = PatientForm(data, instance=patient)
        if form.is_valid():
        	form.save()
        	patientJSON = serializers.serialize("json", [patient])
        	return HttpResponse(patientJSON, content_type='application/json')

        return HttpResponse(status=500)	
