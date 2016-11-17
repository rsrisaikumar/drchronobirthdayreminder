from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

#list of urls with the view names
app_name = 'drchrono_birthday'

urlpatterns=[
	url(r'^$',views.index, name='index'),
	url(r'^guest/', views.guest, name='guest'),
	url(r'^home/', views.home, name='home'),
	url(r'^accounts/error/$', views.error, name='error'),
	url(r'^accounts/logout/$', views.log_out, name='logout'),
	url(r'^email/$', login_required(views.edit_email), name="edit_email"),
	url(r'^patient-search/$', login_required(views.patient_search), name="patient_search"),
    	url(r'^api/doctor/(?P<pk>[0-9]+)/$', login_required(views.DoctorView.as_view()), name='doctor'),
   	url(r'^api/patient/(?P<pk>[0-9]+)/', login_required(views.PatientView.as_view()), name='patient'),
        url(r'^oauth/$', views.oauth, name='oauth'),

]
