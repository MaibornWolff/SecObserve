# Generated by Django 4.2.10 on 2024-02-27 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0031_observation_issue_tracker_issue_closed_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="observation",
            name="assessment_vex_justification",
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
            model_name="observation",
            name="current_vex_justification",
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
            model_name="observation",
            name="parser_vex_justification",
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
            model_name="observation",
            name="rule_vex_justification",
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
            name="vex_justification",
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
    ]
