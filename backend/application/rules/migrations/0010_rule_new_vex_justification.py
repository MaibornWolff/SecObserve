# Generated by Django 4.2.10 on 2024-02-27 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rules", "0009_rule_origin_cloud_qualified_resource"),
    ]

    operations = [
        migrations.AddField(
            model_name="rule",
            name="new_vex_justification",
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
