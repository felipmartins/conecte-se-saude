from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from conectese.forms import (
    NewDailyEvolution,
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
    CalendarDate,
    CreateActivitiesForm,
)
from conectese.models import (
    Patient,
    PhysiotherapyAssessment,
    PhysicalActivityAppointment,
    DailyEvolution,
)
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
        "Ficha de avaliação fisioterapêutica detalhada",
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


@login_required(login_url="/login")
def calendar(request):
    today = date.today()
    today_appointments = PhysicalActivityAppointment.objects.filter(
        date__date=today
    ).order_by("date")
    context = {
        "appointments": today_appointments,
        "today": today,
        "date_form": CalendarDate(),
        "appointment_form": CreateActivitiesForm(),
    }
    return render(request, "calendar/day.html", context)


@login_required(login_url="/login")
def activity_appointment_details(request, activity_appointment_id):
    appointment = PhysicalActivityAppointment.objects.get(id=activity_appointment_id)
    patient_list = list(appointment.patient.all())
    daily_evolution_dict = {
        patient.name: len(
            DailyEvolution.objects.filter(patient=patient, date=appointment.date)
        )
        for patient in patient_list
    }
    context = {
        "appointment": appointment,
        "daily_evolution": daily_evolution_dict,
        "date_form": CalendarDate(),
        "patient_form": SelectPatientForm(),
    }
    return render(request, "calendar/appointment-details.html", context)


@login_required(login_url="/login")
def daily_evolution(request, activity_appointment_id, patient_id):
    appointment = PhysicalActivityAppointment.objects.get(id=activity_appointment_id)
    patient = Patient.objects.get(id=patient_id)
    form = NewDailyEvolution()
    context = {"appointment": appointment, "patient": patient, "form": form}
    if request.method == "POST":
        form = NewDailyEvolution(request.POST)
        if form.is_valid():
            DailyEvolution.objects.create(**form.cleaned_data, date=appointment.date)
            return redirect("activity_appointment_details", activity_appointment_id)
        print(form.errors)
    return render(request, "calendar/daily-evolution.html", context)


@login_required(login_url="/login")
def get_calendar_date(request):
    desired_date = CalendarDate(request.POST)
    if desired_date.is_valid():
        today = desired_date.cleaned_data["date"]
        date_appointments = PhysicalActivityAppointment.objects.filter(
            date__date=today
        ).order_by("date")
        context = {
            "appointments": date_appointments,
            "today": today,
            "date_form": CalendarDate(),
        }
        return render(request, "calendar/day.html", context)

    context = {"patient_form": SelectPatientForm()}
    return render(request, "index.html", context)


@login_required(login_url="/login")
def create_activities(request):
    form = CreateActivitiesForm(request.POST)
    if form.is_valid():
        print(request.POST)
        hours = request.POST.getlist("activities_hours")
        data = form.cleaned_data
        start_date = data["start_date"]
        while start_date <= data["end_date"]:
            for hour in hours:
                if start_date.weekday() >= 5:
                    break
                aux_date = datetime(
                    start_date.year,
                    start_date.month,
                    start_date.day,
                    int(hour[0:2]),
                    0,
                    0,
                )
                PhysicalActivityAppointment.objects.create(date=aux_date)

            start_date = start_date + timedelta(days=1)

        return redirect("calendar")

    else:
        return redirect("calendar")


@login_required(login_url="/login")
def add_patient_to_appointment(request, activity_appointment_id):
    appointment = PhysicalActivityAppointment.objects.get(id=activity_appointment_id)
    form = SelectPatientForm(request.POST)
    if form.is_valid():
        patient = form.cleaned_data["patient"]
        appointment.add_patient(patient)
        return redirect("activity_appointment_details", activity_appointment_id)
    else:
        return redirect("activity_appointment_details", activity_appointment_id)


@login_required(login_url="/login")
def remove_patient_from_appointment(request, activity_appointment_id, patient_id):
    appointment = PhysicalActivityAppointment.objects.get(id=activity_appointment_id)
    patient = Patient.objects.get(id=patient_id)
    appointment.remove_patient(patient)
    return redirect("activity_appointment_details", activity_appointment_id)


@login_required(login_url="/login")
def delete_activity_from_day(request, activity_appointment_id):
    appointment = PhysicalActivityAppointment.objects.get(id=activity_appointment_id)
    date = appointment.date
    appointment.delete()
    return redirect("calendar_date", date=date.strftime("%Y-%m-%d"))


@login_required(login_url="/login")
def calendar_date(request, date):
    date = datetime.strptime(date, "%Y-%m-%d").date()
    date_appointments = PhysicalActivityAppointment.objects.filter(date__date=date)
    context = {
        "appointments": date_appointments,
        "today": date,
        "date_form": CalendarDate(),
    }
    return render(request, "calendar/day.html", context)
