from django import forms
from conectese.models import Patient, MedicalAppointment
from datetime import date


class NewPatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        exclude = ['number_of_lessons']

    def __init__(self, *args, **kwargs):
        super(NewPatientForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Nome do Paciente"
        self.fields["birth_date"].label = "Data de Nascimento"
        self.fields["cpf"].label = "CPF"
        self.fields["contact_phone"].label = "Telefone de Contato"
        self.fields["emergency_phone"].label = "Telefone de Emergência"
        self.fields["civil_status"].label = "Estado Civil"
        self.fields["gender"].label = "Sexo"
        
        self.fields["birth_date"].widget = forms.DateInput(attrs={'type': 'date'})

        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'flex rounded-md w-[200px] h-[25px]'})


class SelectPatientForm(forms.Form):
    patient = forms.ModelChoiceField(label="",queryset=Patient.objects.all(), empty_label="Escolha um paciente",widget=forms.Select(attrs={'class': 'flex rounded-md w-[200px] h-[25px]'}))


class NewMedicalAppointment(forms.ModelForm):

    class Meta:
        model = MedicalAppointment
        fields = ['medical_record', "patient"]

    def __init__(self, *args, **kwargs):
        super(NewMedicalAppointment, self).__init__(*args, **kwargs)
        self.fields["medical_record"].label = "Prontuário"
        self.fields["medical_record"].widget = forms.Textarea(attrs={'class': "w-full mr-4 rounded-xl", 'rows': 20, 'placeholder': '\n  Digite aqui o prontuário do paciente'})
        self.fields["patient"].widget = forms.HiddenInput()
        self.fields["patient"].label = ""
      