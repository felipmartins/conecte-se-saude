from conectese.views import (
    index,
    create_patient,
    show_patient_info,
    get_patient_info,
    medical_appointment,
    create_medical_appointment,
    payment,
    create_payment,
    physio,
    create_physio_assessment,
    calendar,
    activity_appointment_details,
    daily_evolution,
    get_calendar_date,
    create_activities,
    add_patient_to_appointment,
    remove_patient_from_appointment,
    calendar_date,
    delete_activity_from_day,
)
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", index, name="home"),
    path("login", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("patient/new", create_patient, name="create_patient"),
    path("patient/get", get_patient_info, name="get_patient_info"),
    path("patient/info/<int:patient_id>", show_patient_info, name="show_patient_info"),
    path(
        "medical_appointment/new/<int:patient_id>",
        medical_appointment,
        name="medical_appointment",
    ),
    path(
        "medical_appointment/new",
        create_medical_appointment,
        name="create_medical_appointment",
    ),
    path("payment/new/<int:patient_id>", payment, name="payment"),
    path("payment/new", create_payment, name="create_payment"),
    path("physio/new/<int:patient_id>", physio, name="physio"),
    path(
        "physio/all/new/<int:patient_id>",
        create_physio_assessment,
        name="create_physio_assessment",
    ),
    path("calendar", calendar, name="calendar"),
    path(
        "activity_appointment_details/<int:activity_appointment_id>",
        activity_appointment_details,
        name="activity_appointment_details",
    ),
    path(
        "daily_evolution/<int:activity_appointment_id>/<int:patient_id>",
        daily_evolution,
        name="daily_evolution",
    ),
    path(
        "get_calendar_date/",
        get_calendar_date,
        name="get_calendar_date",
    ),
    path(
        "create_activities/",
        create_activities,
        name="create_activities",
    ),
    path(
        "add_patient_to_appointment/<int:activity_appointment_id>",
        add_patient_to_appointment,
        name="add_patient_to_appointment",
    ),
    path(
        "remove_patient_from_appointment/<int:activity_appointment_id>/<int:patient_id>",
        remove_patient_from_appointment,
        name="remove_patient_from_appointment",
    ),
    path(
        "calendar_date/<str:date>",
        calendar_date,
        name="calendar_date",
    ),
    path(
        "delete_activity_from_day/<int:activity_appointment_id>/",
        delete_activity_from_day,
        name="delete_activity_from_day",
    ),
]
