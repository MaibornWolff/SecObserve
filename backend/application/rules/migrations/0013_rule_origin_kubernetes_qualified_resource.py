# Generated by Django 5.0.8 on 2024-08-22 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rules", "0012_alter_rule_parser"),
    ]

    operations = [
        migrations.AddField(
            model_name="rule",
            name="origin_kubernetes_qualified_resource",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
