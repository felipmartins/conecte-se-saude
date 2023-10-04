from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from conectese.forms import NewPatientForm, SelectPatientForm, NewMedicalAppointment
from conectese.models import Patient


@login_required(login_url='/login')
def index(request):
    context = {"patient_form": SelectPatientForm()}
    return render(request, 'index.html', context)

@login_required(login_url='/login')
def create_patient(request):
    form = NewPatientForm()
    if request.method == 'POST':
        form = NewPatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'patient/new.html', {'form': form})

@login_required(login_url='/login')
def get_patient_info(request):
    form = SelectPatientForm(request.POST)
    if form.is_valid():
        patient = form.cleaned_data['patient']
        appointment_type = request.POST.get('appointment_type')
        return_conditions = {'information': redirect('show_patient_info', patient_id=patient.id), 
                             'medical': redirect('medical_appointment', patient_id=patient.id),}
        return return_conditions[appointment_type]
    else:
        return redirect('home')


@login_required(login_url='/login')
def show_patient_info(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    civil_status_dict = { key:value for key, value in Patient.CIVIL_STATUS_CHOICES }
    gender_dict = {key:value for key, value in Patient.GENDER_CHOICES}
    return render(request, 'patient/info.html', {"patient": patient,"gender":gender_dict,"civil":civil_status_dict})


@login_required(login_url='/login')
def medical_appointment(request, patient_id):

    patient = Patient.objects.get(id=patient_id)
    form = NewMedicalAppointment()
    return render(request, 'medical/new-appointment.html', {"patient": patient, "form": form, "today": date.today()})


@login_required(login_url='/login')
def create_medical_appointment(request):
    form = NewMedicalAppointment(request.POST)
    print(form.is_valid)
    print(form.errors)
    if form.is_valid():
        form.save()
        return redirect('home')
    else:
        return redirect('home')