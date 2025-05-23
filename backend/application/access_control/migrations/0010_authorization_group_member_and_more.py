# Generated by Django 5.1.2 on 2024-10-10 11:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("access_control", "0009_user_is_oidc_user"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="ALTER TABLE access_control_authorization_group_users RENAME TO access_control_authorization_group_member",
                    reverse_sql="ALTER TABLE access_control_authorization_group_member RENAME TO access_control_authorization_group_users",
                ),
            ],
            state_operations=[
                migrations.CreateModel(
                    name="Authorization_Group_Member",
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
                        ("is_manager", models.BooleanField(default=False)),
                        (
                            "authorization_group",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                to="access_control.authorization_group",
                            ),
                        ),
                        (
                            "user",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                    ],
                    options={
                        "unique_together": {("authorization_group", "user")},
                    },
                ),
                migrations.AlterField(
                    model_name="authorization_group",
                    name="users",
                    field=models.ManyToManyField(
                        blank=True,
                        related_name="authorization_groups",
                        through="access_control.Authorization_Group_Member",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="authorization_group_member",
            name="is_manager",
            field=models.BooleanField(default=False),
        ),
    ]
