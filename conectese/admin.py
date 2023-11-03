from django.contrib import admin
from conectese.models import (
    Patient,
    PhysiotherapyAssessment,
    MedicalAppointment,
    Payment,
    AssessmentBalance,
    AssessementDailyActivities,
    AssessmentHistory,
    AssessmentMoviment,
    AssessmentPosture,
    AssessmentSensorial,
    AssessmentStrength,
    PhysicalActivityAppointment,
)


# Register your models here.
admin.site.register(Patient)
admin.site.register(PhysiotherapyAssessment)
admin.site.register(MedicalAppointment)
admin.site.register(Payment)
admin.site.register(AssessmentBalance)
admin.site.register(AssessementDailyActivities)
admin.site.register(AssessmentHistory)
admin.site.register(AssessmentMoviment)
admin.site.register(AssessmentPosture)
admin.site.register(AssessmentSensorial)
admin.site.register(AssessmentStrength)
admin.site.register(PhysicalActivityAppointment)
