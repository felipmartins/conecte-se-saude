# Generated by Django 4.2.5 on 2023-10-02 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conectese', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyevolution',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_evolutions', to='conectese.patient'),
        ),
        migrations.AlterField(
            model_name='medicalappointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_appointments', to='conectese.patient'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='conectese.patient'),
        ),
        migrations.RemoveField(
            model_name='physicalactivityappointment',
            name='patient',
        ),
        migrations.AlterField(
            model_name='physiotherapyassessment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='physiotherapy_assessments', to='conectese.patient'),
        ),
        migrations.AddField(
            model_name='physicalactivityappointment',
            name='patient',
            field=models.ManyToManyField(related_name='physical_activity_appointments', to='conectese.patient'),
        ),
    ]
