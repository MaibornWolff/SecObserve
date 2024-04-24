from django.db import migrations


def migrate_settings_data(apps, schema_editor):
    Settings = apps.get_model("commons", "Settings")
    Constance = apps.get_model("constance", "Constance")

    try:
        settings = Settings.objects.get()
    except Settings.DoesNotExist:
        settings = Settings()

    for constance_entry in Constance.objects.all():
        if constance_entry.key == "BACKGROUND_EPSS_IMPORT_CRONTAB_HOURS":
            settings.background_epss_import_crontab_hours = constance_entry.value
        if constance_entry.key == "BACKGROUND_EPSS_IMPORT_CRONTAB_MINUTES":
            settings.background_epss_import_crontab_minutes = constance_entry.value
        if constance_entry.key == "BACKGROUND_PRODUCT_METRICS_INTERVAL_MINUTES":
            settings.background_product_metrics_interval_minutes = constance_entry.value

        if constance_entry.key == "BASE_URL_FRONTEND":
            settings.base_url_frontend = constance_entry.value

        if constance_entry.key == "BRANCH_HOUSEKEEPING_ACTIVE":
            settings.branch_housekeeping_active = constance_entry.value
        if constance_entry.key == "BRANCH_HOUSEKEEPING_CRONTAB_HOURS":
            settings.branch_housekeeping_crontab_hours = constance_entry.value
        if constance_entry.key == "BRANCH_HOUSEKEEPING_CRONTAB_MINUTES":
            settings.branch_housekeeping_crontab_minutes = constance_entry.value
        if constance_entry.key == "BRANCH_HOUSEKEEPING_EXEMPT_BRANCHES":
            settings.branch_housekeeping_exempt_branches = constance_entry.value
        if constance_entry.key == "BRANCH_HOUSEKEEPING_KEEP_INACTIVE_DAYS":
            settings.branch_housekeeping_keep_inactive_days = constance_entry.value

        if constance_entry.key == "EMAIL_FROM":
            settings.email_from = constance_entry.value
        if constance_entry.key == "EXCEPTION_EMAIL_TO":
            settings.exception_email_to = constance_entry.value
        if constance_entry.key == "EXCEPTION_MS_TEAMS_WEBHOOK":
            settings.exception_ms_teams_webhook = constance_entry.value
        if constance_entry.key == "EXCEPTION_RATELIMIT":
            settings.exception_ratelimit = constance_entry.value
        if constance_entry.key == "EXCEPTION_SLACK_WEBHOOK":
            settings.exception_slack_webhook = constance_entry.value

        if constance_entry.key == "FEATURE_VEX":
            settings.feature_vex = constance_entry.value

        if constance_entry.key == "JWT_VALIDITY_DURATION_SUPERUSER":
            settings.jwt_validity_duration_superuser = constance_entry.value
        if constance_entry.key == "JWT_VALIDITY_DURATION_USER":
            settings.jwt_validity_duration_user = constance_entry.value

        if constance_entry.key == "SECURITY_GATE_ACTIVE":
            settings.security_gate_active = constance_entry.value
        if constance_entry.key == "SECURITY_GATE_THRESHOLD_CRITICAL":
            settings.security_gate_threshold_critical = constance_entry.value
        if constance_entry.key == "SECURITY_GATE_THRESHOLD_HIGH":
            settings.security_gate_threshold_high = constance_entry.value
        if constance_entry.key == "SECURITY_GATE_THRESHOLD_MEDIUM":
            settings.security_gate_threshold_medium = constance_entry.value
        if constance_entry.key == "SECURITY_GATE_THRESHOLD_LOW":
            settings.security_gate_threshold_low = constance_entry.value
        if constance_entry.key == "SECURITY_GATE_THRESHOLD_NONE":
            settings.security_gate_threshold_none = constance_entry.value
        if constance_entry.key == "SECURITY_GATE_THRESHOLD_UNKOWN":
            settings.security_gate_threshold_unkown = constance_entry.value

    settings.save()


class Migration(migrations.Migration):
    dependencies = [
        ("commons", "0002_settings"),
        ("constance", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_settings_data),
    ]
