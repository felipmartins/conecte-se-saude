from django.db import models
from conectese.validators import validate_cpf, validate_phone, validate_positive_number


class Patient(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField()
    cpf = models.CharField(max_length=14,  validators=[validate_cpf])
    contact_phone = models.CharField(max_length=10, validators=[validate_phone]) 
    emergency_phone = models.CharField(max_length=10, validators=[validate_phone]) 
    civil_status = models.CharField(max_length=20, choices=[('single', 'Solteiro(a)'), ('married', 'Casado(a)'), ('divorced', 'Divorciado(a)'), ('widower', 'Viúvo(a)')])
    gender = models.CharField(max_length=10, choices=[('male', 'Masculino'),('female', 'Feminino')])
    number_of_lessons = models.IntegerField(default=0, validators=[validate_positive_number])

    def __str__(self):
        return self.name
    

class MedicalAppointment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_appointments')
    medical_record = models.TextField()

    def __str__(self):
        return str(self.date)


class PhysicalActivityAppointment(models.Model):
    date = models.DateTimeField()
    patient = models.ManyToManyField(Patient, related_name='physical_activity_appointments')

    def add_patient(self, patient):
        self.patient.add(patient)
        self.save()
    
    def remove_patient(self, patient):
        self.patient.remove(patient)
        self.save()

    def __str__(self):
        return str(self.date)


class Payment(models.Model):
    registration_date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments')
    times_per_week = models.CharField(max_length=50, choices=[('1', '1x por semana'), ('2', '2x por semana'), ('3', '3x por semana'), ('4', '4x por semana'), ('5', '5x por semana')])
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_day = models.DateField()

    def add_lessons_to_patient(self):
        self.patient.number_of_lessons += int(int(self.times_per_week)*4.5)
        self.patient.save()

    def __str__(self):
        return f"{self.patient} - {self.payment_amount}"
    

class PhysiotherapyAssessment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='physiotherapy_assessments')

    main_plainte = models.TextField()
    avant_history = models.TextField()
    actual_history = models.TextField()
    previous_blessures = models.TextField()
    cirurgic_history = models.TextField()

    general_observation = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('altered', 'Alterada'), ('other', 'Outra')])
    other_observation = models.TextField()
    head_alligment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('anteriorized', 'Anteriorizada'), ('side_inclination','Inclinada para um lado'),('other', 'Outro')])
    head_observation = models.TextField()
    shoulder_alligment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('elevated', 'Elevados'), ('intern_rotation','Rotação interna'), ('extern_rotation','Rotação externa'),('other', 'Outro')])
    shoulder_observation = models.TextField()
    collumn_alligment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('hiperlordosis', 'Hiperlordose'), ('hipercifosis','Hipercifose'),('scoliosis','Escoliose'),('other', 'Outro')])
    collumn_observation = models.TextField()
    pelvis_alligment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('anterior_inclination', 'Inclinação anterior'), ('posterior_inclination','Inclinação posterior'),('side_inclination','Inclinação lateral'),('other', 'Outro')])
    pelvis_observation = models.TextField()
    superior_and_inferior_members = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('detour', 'Desvio'), ('other', 'Outro')])
    superior_and_inferior_members_observation = models.TextField()

    cervical_moviment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('restrict', 'Restrita'),('other', 'Outra')])
    cervical_moviment_observation = models.TextField()
    shoulder_moviment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('restrict', 'Restrita'),('other', 'Outra')])
    shoulder_moviment_observation = models.TextField()
    elbow_moviment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('restrict', 'Restrita'),('other', 'Outra')])
    elbow_moviment_observation = models.TextField()
    wrist_and_hand_moviment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('restrict', 'Restrita'),('other', 'Outra')])
    wrist_and_hand_moviment_observation = models.TextField()
    spinal_moviment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('restrict', 'Restrita'),('other', 'Outra')])
    spinal_moviment_observation = models.TextField()
    hip_moviment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('restrict', 'Restrita'),('other', 'Outra')])
    hip_moviment_observation = models.TextField()
    knee_moviment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('restrict', 'Restrita'),('other', 'Outra')])
    knee_moviment_observation = models.TextField()
    ankle_and_foot_moviment = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('restrict', 'Restrita'),('other', 'Outra')])
    ankle_and_foot_moviment_observation = models.TextField()

    cervical_strength = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('weak', 'Fraca'),('other', 'Outra')])
    cervical_strength_observation = models.TextField()
    shoulder_strength = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('weak', 'Fraca'),('other', 'Outra')])
    shoulder_strength_observation = models.TextField()
    elbow_strength = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('weak', 'Fraca'),('other', 'Outra')])
    elbow_strength_observation = models.TextField()
    wrist_and_hand_strength = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('weak', 'Fraca'),('other', 'Outra')])
    wrist_and_hand_strength_observation = models.TextField()
    spinal_strength = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('weak', 'Fraca'),('other', 'Outra')])
    spinal_strength_observation = models.TextField()
    hip_strength = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('weak', 'Fraca'),('other', 'Outra')])
    hip_strength_observation = models.TextField()
    knee_strength = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('weak', 'Fraca'),('other', 'Outra')])
    knee_strength_observation = models.TextField()
    ankle_and_foot_strength = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('weak', 'Fraca'),('other', 'Outra')])
    ankle_and_foot_strength_observation = models.TextField()

    tactile_sensitivity = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('altered', 'Alterada'),('other', 'Outra')])
    tactile_sensitivity_observation = models.TextField()
    termic_sensitivity = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('altered', 'Alterada'),('other', 'Outra')])
    termic_sensitivity_observation = models.TextField()
    painful_sensitivity = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('altered', 'Alterada'),('other', 'Outra')])
    painful_sensitivity_observation = models.TextField()

    static_balance = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('altered', 'Alterado'),('other', 'Outro')])
    static_balance_observation = models.TextField()
    dinamic_balance = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('altered', 'Alterado'),('other', 'Outro')])
    dinamic_balance_observation = models.TextField()
    march = models.CharField(max_length=50, choices=[('normal', 'Normal'), ('altered', 'Alterada'),('other', 'Outra')])
    march_observation = models.TextField()

    personal_hygiene = models.CharField(max_length=50, choices=[('independent', 'Independente'), ('dependent', 'Dependente'),('partial_assistence','Assistência parcial'),('other', 'Outra')])
    personal_hygiene_observation = models.TextField()
    dressing = models.CharField(max_length=50, choices=[('independent', 'Independente'), ('dependent', 'Dependente'),('partial_assistence','Assistência parcial'),('other', 'Outra')])
    dressing_observation = models.TextField()
    feeding = models.CharField(max_length=50, choices=[('independent', 'Independente'), ('dependent', 'Dependente'),('partial_assistence','Assistência parcial'),('other', 'Outra')])
    feeding_observation = models.TextField()
    locomotion = models.CharField(max_length=50, choices=[('independent', 'Independente'), ('dependent', 'Dependente'),('partial_assistence','Assistência parcial'),('other', 'Outra')])
    locomotion_observation = models.TextField()
    other_activities = models.TextField()

    objectives = models.TextField()

    conducts = models.TextField()

    observations_and_final_comments = models.TextField()

    def __str__(self):
        return f"{self.patient} - {self.date}"
    

    class DailyEvolution(models.Model):
        patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='daily_evolutions')
        date = models.DateTimeField(auto_now_add=True)
        presence = models.CharField(max_length=50, choices=[('present', 'Presente'), ('absent', 'Ausente')])
        pain_plainte = models.TextField()
        equipment = models.CharField(max_length=50, choices=[('reformer', 'Reformer'), ('barrel', 'Barrel'),('cadillac', 'Cadillac'), ('chair', 'Chair'), ('wall_chair', 'Wall Chair'), ('solo', 'Solo')])
        stretching = models.CharField(max_length=50, choices=[('superior', 'Membros Superiores'), ('inferior', 'Membros Inferiores'),('other', 'Outro')])
        strengthening = models.CharField(max_length=50, choices=[('superior', 'Membros Superiores'), ('inferior', 'Membros Inferiores'),('other', 'Outro')])
        other_conducts = models.TextField()
        observations = models.TextField()


        def reduce_one_lesson(self):
            self.patient.number_of_lessons -= 1
            self.patient.save()

        def __str__(self):
            return f"{self.patient} - {self.date}"

        
