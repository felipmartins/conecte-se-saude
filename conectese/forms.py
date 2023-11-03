from django import forms
from conectese.models import (
    DailyEvolution,
    Patient,
    MedicalAppointment,
    Payment,
    PhysiotherapyAssessment,
    AssessementDailyActivities,
    AssessmentBalance,
    AssessmentHistory,
    AssessmentMoviment,
    AssessmentPosture,
    AssessmentSensorial,
    AssessmentStrength,
)
from datetime import date


class NewPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ["number_of_lessons", "pay_day"]

    def __init__(self, *args, **kwargs):
        super(NewPatientForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Nome do Paciente"
        self.fields["birth_date"].label = "Data de Nascimento"
        self.fields["cpf"].label = "CPF"
        self.fields["contact_phone"].label = "Telefone de Contato"
        self.fields["emergency_phone"].label = "Telefone de Emergência"
        self.fields["civil_status"].label = "Estado Civil"
        self.fields["gender"].label = "Sexo"

        self.fields["birth_date"].widget = forms.DateInput(
            attrs={"type": "date"},
        )

        for key in self.fields:
            self.fields[key].widget.attrs.update(
                {"class": "flex rounded-md w-[200px] h-[25px] pl-1"}
            )


class SelectPatientForm(forms.Form):
    patient = forms.ModelChoiceField(
        label="",
        queryset=Patient.objects.all(),
        empty_label="Escolha um paciente",
        widget=forms.Select(
            attrs={"class": "flex rounded-md w-[200px] h-[25px]"},
        ),
    )


class NewMedicalAppointment(forms.ModelForm):
    class Meta:
        model = MedicalAppointment
        fields = ["medical_record", "patient"]

    def __init__(self, *args, **kwargs):
        super(NewMedicalAppointment, self).__init__(*args, **kwargs)
        self.fields["medical_record"].label = "Prontuário"
        self.fields["medical_record"].widget = forms.Textarea(
            attrs={
                "class": "w-full mr-4 rounded-xl pl-2 pt-2",
                "rows": 20,
                "placeholder": "Digite aqui o prontuário do paciente",
            }
        )
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""


class NewPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["pay_day", "times_per_week", "payment_amount", "patient"]

    def __init__(self, *args, **kwargs):
        super(NewPaymentForm, self).__init__(*args, **kwargs)
        self.fields["times_per_week"].label = "Número de vezes por semana"
        self.fields["payment_amount"].label = "Valor"
        self.fields["pay_day"].label = "Dia do vencimento"
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        for key in self.fields:
            self.fields[key].widget.attrs.update(
                {"class": "flex rounded-md w-[200px] h-[25px] text-center pl-1"}
            )


class NewPhysioterapyAssessment(forms.ModelForm):
    class Meta:
        model = PhysiotherapyAssessment
        exclude = [
            "date",
            "patient_history",
            "patient_posture",
            "patient_moviment",
            "patient_balance",
            "patient_sensitivity",
            "patient_strength",
            "patient_activities",
        ]

    def __init__(self, *args, **kwargs):
        super(NewPhysioterapyAssessment, self).__init__(*args, **kwargs)
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        text_fields = ["objectives", "conducts", "observations_and_final_comments"]

        for field in text_fields:
            self.fields[field].widget = forms.Textarea(
                attrs={
                    "class": "w-full mr-2 rounded-xl pl-2 pt-2",
                    "rows": 2,
                    "placeholder": "Digite aqui",
                }
            )

        self.fields["objectives"].label = "Objetivos"
        self.fields["conducts"].label = "Condutas"
        self.fields[
            "observations_and_final_comments"
        ].label = "Observações e considerações finais"


class NewAssessementDailyActivities(forms.ModelForm):
    class Meta:
        model = AssessementDailyActivities
        exclude = ["date"]

    def __init__(self, *args, **kwargs):
        super(NewAssessementDailyActivities, self).__init__(*args, **kwargs)
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        text_fields = [
            "personal_hygiene_observation",
            "dressing_observation",
            "feeding_observation",
            "locomotion_observation",
            "other_activities",
        ]

        select_fields = [
            "personal_hygiene",
            "dressing",
            "feeding",
            "locomotion",
        ]

        for field in text_fields:
            self.fields[field].widget = forms.Textarea(
                attrs={
                    "class": "w-full mr-2 rounded-xl pl-2 pt-2",
                    "rows": 2,
                    "placeholder": 'Se selecionou "Outro(a)", digite aqui as observações',
                }
            )
            self.fields[field].label = "Outro"

        for field in select_fields:
            self.fields[field].widget.attrs = {
                "class": "flex rounded-md w-[200px] h-[25px] text-center"
            }

        self.fields["other_activities"].label = "Outras atividades"
        self.fields["other_activities"].widget.attrs = {
            "class": "w-full mr-2 rounded-xl pl-1",
            "rows": 2,
            "placeholder": " Digite aqui sobre outras atividades",
        }

        self.fields["personal_hygiene"].label = "Higiene pessoal"
        self.fields["dressing"].label = "Vestir-se"
        self.fields["feeding"].label = "Alimentação"
        self.fields["locomotion"].label = "Locomoção"


class NewAssessmentBalance(forms.ModelForm):
    class Meta:
        model = AssessmentBalance
        exclude = ["date"]

    def __init__(self, *args, **kwargs):
        super(NewAssessmentBalance, self).__init__(*args, **kwargs)
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        text_fields = [
            "static_balance_observation",
            "dinamic_balance_observation",
            "march_observation",
        ]

        select_fields = [
            "static_balance",
            "dinamic_balance",
            "march",
        ]

        for field in text_fields:
            self.fields[field].widget = forms.Textarea(
                attrs={
                    "class": "w-full mr-2 rounded-xl pl-2 pt_2",
                    "rows": 2,
                    "placeholder": 'Se selecionou "Outro(a)", digite aqui as observações',
                }
            )
            self.fields[field].label = "Outro"

        for field in select_fields:
            self.fields[field].widget.attrs = {
                "class": "flex rounded-md w-[200px] h-[25px] text-center"
            }

        self.fields["static_balance"].label = "Equilíbrio estático"
        self.fields["dinamic_balance"].label = "Equilíbrio dinâmico"
        self.fields["march"].label = "Marcha"


class NewAssessmentHistory(forms.ModelForm):
    class Meta:
        model = AssessmentHistory
        exclude = ["date"]

    def __init__(self, *args, **kwargs):
        super(NewAssessmentHistory, self).__init__(*args, **kwargs)
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        text_fields = [
            "main_plainte",
            "avant_history",
            "actual_history",
            "previous_blessures",
            "cirurgic_history",
        ]

        for field in text_fields:
            self.fields[field].widget = forms.Textarea(
                attrs={
                    "class": "w-full mr-2 rounded-xl pl-2 pt-2",
                    "rows": 2,
                    "placeholder": "Digite aqui",
                }
            )

        self.fields["main_plainte"].label = "Queixa principal"
        self.fields["avant_history"].label = "História pregressa"
        self.fields["actual_history"].label = "História atual"
        self.fields["previous_blessures"].label = "História de lesões prévias"
        self.fields["cirurgic_history"].label = "História cirúrgica"


class NewAssessmentMoviment(forms.ModelForm):
    class Meta:
        model = AssessmentMoviment
        exclude = ["date"]

    def __init__(self, *args, **kwargs):
        super(NewAssessmentMoviment, self).__init__(*args, **kwargs)
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        text_fields = [
            "cervical_moviment_observation",
            "shoulder_moviment_observation",
            "elbow_moviment_observation",
            "wrist_and_hand_moviment_observation",
            "spinal_moviment_observation",
            "hip_moviment_observation",
            "knee_moviment_observation",
            "ankle_and_foot_moviment_observation",
        ]

        select_fields = [
            "cervical_moviment",
            "shoulder_moviment",
            "elbow_moviment",
            "wrist_and_hand_moviment",
            "spinal_moviment",
            "hip_moviment",
            "knee_moviment",
            "ankle_and_foot_moviment",
        ]

        for field in text_fields:
            self.fields[field].widget = forms.Textarea(
                attrs={
                    "class": "w-full mr-2 rounded-xl pl-2 pt-2",
                    "rows": 2,
                    "placeholder": 'Se selecionou "Outro(a)", digite aqui as observações',
                }
            )
            self.fields[field].label = "Outro"

        for field in select_fields:
            self.fields[field].widget.attrs = {
                "class": "flex rounded-md w-[200px] h-[25px] text-center"
            }

        self.fields["cervical_moviment"].label = "Cervical"
        self.fields["shoulder_moviment"].label = "Ombro"
        self.fields["elbow_moviment"].label = "Cotovelo"
        self.fields["wrist_and_hand_moviment"].label = "Punho e mão"
        self.fields["spinal_moviment"].label = "Coluna vertebral"
        self.fields["hip_moviment"].label = "Quadril"
        self.fields["knee_moviment"].label = "Joelho"
        self.fields["ankle_and_foot_moviment"].label = "Tornozelo e pé"


class NewAssessmentPosture(forms.ModelForm):
    class Meta:
        model = AssessmentPosture
        exclude = ["date"]

    def __init__(self, *args, **kwargs):
        super(NewAssessmentPosture, self).__init__(*args, **kwargs)
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        text_fields = [
            "other_observation",
            "head_observation",
            "shoulder_observation",
            "collumn_observation",
            "pelvis_observation",
            "superior_and_inferior_members_observation",
        ]

        select_fields = [
            "general_observation",
            "head_alligment",
            "shoulder_alligment",
            "collumn_alligment",
            "pelvis_alligment",
            "superior_and_inferior_members",
        ]

        for field in text_fields:
            self.fields[field].widget = forms.Textarea(
                attrs={
                    "class": "w-full mr-2 rounded-xl pl-2 pt-2",
                    "rows": 2,
                    "placeholder": 'Se selecionou "Outro(a)", digite aqui as observações',
                }
            )
            self.fields[field].label = "Outro"

        for field in select_fields:
            self.fields[field].widget.attrs = {
                "class": "flex rounded-md w-[200px] h-[25px] text-center"
            }

        self.fields["general_observation"].label = "Observações gerais"
        self.fields["head_alligment"].label = "Alinhamento da cabeça"
        self.fields["shoulder_alligment"].label = "Alinhamento dos ombros"
        self.fields["collumn_alligment"].label = "Alinhamento da coluna vertebral"
        self.fields["pelvis_alligment"].label = "Alinhamento da pelve"
        self.fields[
            "superior_and_inferior_members"
        ].label = "Alinhamento dos membros superiores e inferiores"


class NewAssessmentSensorial(forms.ModelForm):
    class Meta:
        model = AssessmentSensorial
        exclude = ["date"]

    def __init__(self, *args, **kwargs):
        super(NewAssessmentSensorial, self).__init__(*args, **kwargs)
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        text_fields = [
            "tactile_sensitivity_observation",
            "termic_sensitivity_observation",
            "painful_sensitivity_observation",
        ]

        select_fields = [
            "tactile_sensitivity",
            "termic_sensitivity",
            "painful_sensitivity",
        ]

        for field in text_fields:
            self.fields[field].widget = forms.Textarea(
                attrs={
                    "class": "w-full mr-2 rounded-xl pl-2 pt-2",
                    "rows": 2,
                    "placeholder": 'Se selecionou "Outro(a)", digite aqui as observações',
                }
            )
            self.fields[field].label = "Outro"

        for field in select_fields:
            self.fields[field].widget.attrs = {
                "class": "flex rounded-md w-[200px] h-[25px] text-center"
            }

        self.fields["tactile_sensitivity"].label = "Sensibilidade tátil"
        self.fields["termic_sensitivity"].label = "Sensibilidade térmica"
        self.fields["painful_sensitivity"].label = "Sensibilidade dolorosa"


class NewAssessmentStrength(forms.ModelForm):
    class Meta:
        model = AssessmentStrength
        exclude = ["date"]

    def __init__(self, *args, **kwargs):
        super(NewAssessmentStrength, self).__init__(*args, **kwargs)
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        text_fields = [
            "cervical_strength_observation",
            "shoulder_strength_observation",
            "elbow_strength_observation",
            "wrist_and_hand_strength_observation",
            "spinal_strength_observation",
            "hip_strength_observation",
            "knee_strength_observation",
            "ankle_and_foot_strength_observation",
        ]

        select_fields = [
            "cervical_strength",
            "shoulder_strength",
            "elbow_strength",
            "wrist_and_hand_strength",
            "spinal_strength",
            "hip_strength",
            "knee_strength",
            "ankle_and_foot_strength",
        ]

        for field in text_fields:
            self.fields[field].widget = forms.Textarea(
                attrs={
                    "class": "w-full mr-2 rounded-xl pl-2 pt-2",
                    "rows": 2,
                    "placeholder": 'Se selecionou "Outro(a)", digite aqui as observações',
                }
            )
            self.fields[field].label = "Outro"

        for field in select_fields:
            self.fields[field].widget.attrs = {
                "class": "flex rounded-md w-[200px] h-[25px] text-center"
            }

        self.fields["cervical_strength"].label = "Músculos cervicais"
        self.fields["shoulder_strength"].label = "Músculos do ombros"
        self.fields["elbow_strength"].label = "Músculos do cotovelo"
        self.fields["wrist_and_hand_strength"].label = "Músculos do punho e mão"
        self.fields["spinal_strength"].label = "Músculos da coluna vertebral"
        self.fields["hip_strength"].label = "Músculos do quadril"
        self.fields["knee_strength"].label = "Músculos do joelho"
        self.fields["ankle_and_foot_strength"].label = "Músculos do tornozelo e pé"


class NewDailyEvolution(forms.ModelForm):
    class Meta:
        model = DailyEvolution
        exclude = ["date"]

    def __init__(self, *args, **kwargs):
        super(NewDailyEvolution, self).__init__(*args, **kwargs)
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""

        text_fields = ["pain_plainte", "other_conducts", "observations"]

        select_fields = [
            "presence",
            "equipment",
            "stretching",
            "strengthening",
        ]

        for field in text_fields:
            self.fields[field].widget = forms.Textarea(
                attrs={
                    "class": "w-full mr-2 rounded-xl pl-2 pt-2",
                    "rows": 2,
                    "placeholder": "Digite aqui",
                }
            )

        for field in select_fields:
            self.fields[field].widget.attrs = {
                "class": "flex rounded-md w-[200px] h-[25px] text-center"
            }

        self.fields["presence"].label = "Presença"
        self.fields["equipment"].label = "Equipamentos"
        self.fields["stretching"].label = "Alongamentos"
        self.fields["strengthening"].label = "Fortalecimento"
        self.fields["pain_plainte"].label = "Queixa de dor"
        self.fields["other_conducts"].label = "Outras condutas"
        self.fields["observations"].label = "Observações"


class CalendarDate(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "flex rounded-md w-[120px] pl-2"}
        ),
        label="",
        initial=date.today(),
    )
