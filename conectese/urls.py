from conectese.views import index, create_patient, show_patient_info, get_patient_info, medical_appointment, create_medical_appointment
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
    path('', index, name='home'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('patient/new', create_patient, name='create_patient'),
    path('patient/get', get_patient_info, name='get_patient_info'),
    path('patient/info/<int:patient_id>', show_patient_info, name='show_patient_info'),
    path('medical_appointment/new/<int:patient_id>', medical_appointment, name='medical_appointment'),
    path('medical_appointment/new', create_medical_appointment, name='create_medical_appointment'),
]