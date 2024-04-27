# Generated by Django 4.2.11 on 2024-04-25 20:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rules", "0010_rule_new_vex_justification"),
        ("core", "0038_alter_observation_log_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="observation_log",
            name="general_rule",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="observation_log_general_rules",
                to="rules.rule",
            ),
        ),
        migrations.AddField(
            model_name="observation_log",
            name="product_rule",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="observation_log_product_rules",
                to="rules.rule",
            ),
        ),
    ]
