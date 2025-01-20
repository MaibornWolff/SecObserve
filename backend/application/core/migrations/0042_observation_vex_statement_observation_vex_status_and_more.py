# Generated by Django 5.0.6 on 2024-06-13 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0041_parser_class_name_parser_module_name"),
        ("vex", "0006_vex_document_vex_statement"),
    ]

    operations = [
        migrations.AddField(
            model_name="observation",
            name="vex_statement",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="vex_statements",
                to="vex.vex_statement",
            ),
        ),
        migrations.AddField(
            model_name="observation",
            name="vex_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Open", "Open"),
                    ("Resolved", "Resolved"),
                    ("Duplicate", "Duplicate"),
                    ("False positive", "False positive"),
                    ("In review", "In review"),
                    ("Not affected", "Not affected"),
                    ("Not security", "Not security"),
                    ("Risk accepted", "Risk accepted"),
                ],
                max_length=16,
            ),
        ),
        migrations.AddField(
            model_name="observation",
            name="vex_vex_justification",
            field=models.CharField(
                blank=True,
                choices=[
                    ("component_not_present", "Component not present"),
                    ("vulnerable_code_not_present", "Vulnerable code not present"),
                    (
                        "vulnerable_code_cannot_be_controlled_by_adversary",
                        "Vulnerable code cannot be controlled by adversary",
                    ),
                    (
                        "vulnerable_code_not_in_execute_path",
                        "Vulnerable code not in execute path",
                    ),
                    (
                        "inline_mitigations_already_exist",
                        "Inline mitigations already exist",
                    ),
                ],
                max_length=64,
            ),
        ),
        migrations.AddField(
            model_name="observation_log",
            name="vex_statement",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="observation_log_vex_statements",
                to="vex.vex_statement",
            ),
        ),
    ]