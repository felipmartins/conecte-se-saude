from datetime import date


def check_current_step_physio_evaluation(patient):
    history = patient.assessment_history.all().filter(date=date.today())
    posture = patient.assessment_posture.all().filter(date=date.today())
    moviment = patient.assessment_moviment.all().filter(date=date.today())
    strength = patient.assessment_strength.all().filter(date=date.today())
    sensorial = patient.assessment_sensorial.all().filter(date=date.today())
    balance = patient.assessment_balance.all().filter(date=date.today())
    daily_activities = patient.assessment_evolutions.all().filter(date=date.today())
    physio_assessment = patient.physiotherapy_assessments.all().filter(date=date.today())

    routine = [
        history,
        posture,
        moviment,
        strength,
        sensorial,
        balance,
        daily_activities,
        physio_assessment,
    ]

    for index, step in enumerate(routine):
        if not step:
            return index
    
    return "created"
    
    
