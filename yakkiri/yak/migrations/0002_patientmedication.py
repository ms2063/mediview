# Generated by Django 5.0.6 on 2024-05-29 03:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("medicine", "0001_initial"),
        ("yak", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientMedication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dosage", models.CharField(max_length=100)),
                ("frequency", models.CharField(max_length=100)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="medications",
                        to="yak.patientinfo",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="medicine.제품"
                    ),
                ),
            ],
        ),
    ]