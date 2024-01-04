from django.db import migrations


def rename_zap_parser(apps, schema_editor):
    Parser = apps.get_model("core", "Parser")
    try:
        owasp_zap_parser = Parser.objects.get(name="OWASP ZAP")
    except Parser.DoesNotExist:
        owasp_zap_parser = None

    try:
        zap_parser = Parser.objects.get(name="ZAP")
    except Parser.DoesNotExist:
        zap_parser = None

    if owasp_zap_parser and zap_parser:
        # A new parser with the name "ZAP" has been created during startup, we have to delete it
        zap_parser.delete()

    if owasp_zap_parser:
        # Rename the existing "OWASP ZAP" parser to "ZAP"
        owasp_zap_parser.name = "ZAP"
        owasp_zap_parser.save()


class Migration(migrations.Migration):
    dependencies = [
        ("import_observations", "0003_alter_vulnerability_check_branch"),
    ]

    operations = [
        migrations.RunPython(rename_zap_parser),
    ]
