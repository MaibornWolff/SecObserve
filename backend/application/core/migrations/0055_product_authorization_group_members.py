# Generated by Django 5.1.3 on 2024-11-18 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("access_control", "0010_authorization_group_member_and_more"),
        ("core", "0054_convert_unknown_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="authorization_group_members",
            field=models.ManyToManyField(
                blank=True,
                related_name="authorization_groups",
                through="core.Product_Authorization_Group_Member",
                to="access_control.authorization_group",
            ),
        ),
    ]
