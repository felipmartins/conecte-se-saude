from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from conectese.forms import (
    NewPatientForm,
    SelectPatientForm,
    NewMedicalAppointment,
    NewPaymentForm,
    NewPhysioterapyAssessment,
    NewAssessementDailyActivities,
    NewAssessmentBalance,
    NewAssessmentHistory,
    NewAssessmentMoviment,
    NewAssessmentPosture,
    NewAssessmentSensorial,
    NewAssessmentStrength,
)
from conectese.models import Patient, PhysiotherapyAssessment
from conectese.utils import check_current_step_physio_evaluation


@login_required(login_url="/login")
def index(request):
    context = {"patient_form": SelectPatientForm()}
    return render(request, "index.html", context)


@login_required(login_url="/login")
def create_patient(request):
    form = NewPatientForm()
    if request.method == "POST":
        form = NewPatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "patient/new.html", {"form": form})


@login_required(login_url="/login")
def get_patient_info(request):
    form = SelectPatientForm(request.POST)
    if form.is_valid():
        patient = form.cleaned_data["patient"]
        appointment_type = request.POST.get("appointment_type")
        return_conditions = {
            "information": redirect("show_patient_info", patient_id=patient.id),
            "medical": redirect("medical_appointment", patient_id=patient.id),
            "payment": redirect("payment", patient_id=patient.id),
            "physio": redirect("physio", patient_id=patient.id),
        }
        return return_conditions[appointment_type]
    else:
        return redirect("home")


@login_required(login_url="/login")
def show_patient_info(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    civil_status_dict = {key: value for key, value in Patient.CIVIL_STATUS_CHOICES}
    gender_dict = {key: value for key, value in Patient.GENDER_CHOICES}
    return render(
        request,
        "patient/info.html",
        {"patient": patient, "gender": gender_dict, "civil": civil_status_dict},
    )


@login_required(login_url="/login")
def medical_appointment(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    form = NewMedicalAppointment()
    return render(
        request,
        "medical/new-appointment.html",
        {"patient": patient, "form": form, "today": date.today()},
    )


@login_required(login_url="/login")
def create_medical_appointment(request):
    form = NewMedicalAppointment(request.POST)
    print(form.is_valid)
    print(form.errors)
    if form.is_valid():
        form.save()
        return redirect("home")
    else:
        return redirect("home")


@login_required(login_url="/login")
def payment(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    form = NewPaymentForm()
    if patient.pay_day:
        form.fields["pay_day"].initial = patient.pay_day
    else:
        form.fields["pay_day"].initial = "1"

    return render(
        request,
        "payment/new.html",
        {"patient": patient, "today": date.today(), "form": form},
    )


@login_required(login_url="/login")
def create_payment(request):
    form = NewPaymentForm(request.POST)

    if form.is_valid():
        form.save()
        patient = Patient.objects.get(id=form.instance.patient.id)

        if not patient.pay_day:
            form.instance.set_pay_day()

        form.instance.add_lessons_to_patient()

        return redirect("home")
    else:
        return redirect("home")


@login_required(login_url="/login")
def physio(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    evaluation_form = NewPhysioterapyAssessment
    history_form = NewAssessmentHistory
    posture_form = NewAssessmentPosture
    moviment_form = NewAssessmentMoviment
    strength_form = NewAssessmentStrength
    sensorial_form = NewAssessmentSensorial
    balance_form = NewAssessmentBalance
    daily_activities_form = NewAssessementDailyActivities

    forms_order = [
        history_form,
        posture_form,
        moviment_form,
        strength_form,
        sensorial_form,
        balance_form,
        daily_activities_form,
        evaluation_form,
    ]
    button_text = [
        "Avançar",
        "Avançar",
        "Avançar",
        "Avançar",
        "Avançar",
        "Avançar",
        "Avançar",
        "Finalizar",
    ]

    form_title = [
        "Avaliação de histórico",
        "Avaliação da postura",
        "Avaliação da amplitude de movimento (AM)",
        "Avaliação da força muscular",
        "Avaliação da sensibilidade",
        "Avaliação do equilíbrio e marcha",
        "Avaliação das atividades de vida diária (AVDs)",
        "Ficha de avaliação fisioterapêutica detalhada"
    ]

    step = check_current_step_physio_evaluation(patient)

    if step == "created":
        return redirect("home")

    if request.method == "POST":
        form = forms_order[step](request.POST)
        print(forms_order[step])
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect("physio", patient_id=patient.id)
        else:
            return redirect("home")

    return render(
        request,
        "physio/new-evaluation.html",
        {
            "patient": patient,
            "today": date.today(),
            "form": forms_order[step](),
            "button_text": button_text[step],
            "form_title": form_title[step],
        },
    )


@login_required(login_url="/login")
def create_physio_assessment(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    form = NewPhysioterapyAssessment(request.POST)

    if form.is_valid():
        PhysiotherapyAssessment.objects.create(
            patient=patient,
            patient_history=patient.assessment_history.all().last(),
            patient_posture=patient.assessment_posture.all().last(),
            patient_moviment=patient.assessment_moviment.all().last(),
            patient_strength=patient.assessment_strength.all().last(),
            patient_sensitivity=patient.assessment_sensorial.all().last(),
            patient_balance=patient.assessment_balance.all().last(),
            patient_activities=patient.assessment_evolutions.all().last(),
            objectives=form.cleaned_data["objectives"],
            conducts=form.cleaned_data["conducts"],
            observations_and_final_comments=form.cleaned_data[
                "observations_and_final_comments"
            ],
        )

        return redirect("home")
    else:
        return redirect("physio", patient_id=patient.id)
