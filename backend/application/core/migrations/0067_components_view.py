from django.db import migrations

CREATE_SQL = """
DROP VIEW IF EXISTS core_component;
CREATE VIEW core_component AS
WITH CombinedData AS (
    SELECT
        product_id as product_id,
        branch_id as branch_id,
        origin_service_id as origin_service_id,
        origin_component_name AS component_name,
        origin_component_version AS component_version,
        origin_component_name_version AS component_name_version,
        origin_component_purl AS component_purl,
        origin_component_purl_type AS component_purl_type,
        origin_component_cpe AS component_cpe,
        origin_component_dependencies AS component_dependencies,
        origin_component_cyclonedx_bom_link AS component_cyclonedx_bom_link
    FROM core_observation
    WHERE origin_component_name_version != ''

    UNION
    
    SELECT 
        product_id as product_id,
        branch_id as branch_id,
        origin_service_id as origin_service_id,
        component_name AS component_name,
        component_version AS component_version,
        component_name_version AS component_name_version,
        component_purl AS component_purl,
        component_purl_type AS component_purl_type,
        component_cpe AS component_cpe,
        component_dependencies AS component_dependencies,
        component_cyclonedx_bom_link AS component_cyclonedx_bom_link
    FROM licenses_license_component
),
ObservationFlag AS (
    SELECT DISTINCT
        product_id,
        branch_id,
        origin_service_id,
        origin_component_name_version AS component_name_version,
        origin_component_purl_type AS component_purl_type,
        TRUE AS has_observation
    FROM core_observation
)
SELECT 
    MD5(
		CONCAT(
			CAST(COALESCE(cd.product_id, 111) as CHAR(255)),
			CAST(COALESCE(cd.branch_id, 222) as CHAR(255)),
			CAST(COALESCE(cd.origin_service_id, 333) as CHAR(255)),
			COALESCE(cd.component_name_version, 'no_name_version'),
			COALESCE(cd.component_purl_type, 'no_purl_type'),
			COALESCE(cd.component_dependencies, 'no_dependencies')
			)		
		) AS id,
    cd.product_id as product_id,
    cd.branch_id as branch_id,
    cd.origin_service_id as origin_service_id,
    cd.component_name AS component_name,
    cd.component_version AS component_version,
    cd.component_name_version AS component_name_version,
    cd.component_purl AS component_purl,
    cd.component_purl_type AS component_purl_type,
    cd.component_cpe AS component_cpe,
    cd.component_dependencies AS component_dependencies,
    cd.component_cyclonedx_bom_link AS component_cyclonedx_bom_link,
    COALESCE(ObservationFlag.has_observation, FALSE) AS has_observations
FROM CombinedData cd
LEFT JOIN ObservationFlag ON 
    cd.product_id = ObservationFlag.product_id
	AND (
        (cd.branch_id = ObservationFlag.branch_id) IS TRUE OR 
        (cd.branch_id IS NULL AND ObservationFlag.branch_id IS NULL)
        )
	AND (
        (cd.origin_service_id = ObservationFlag.origin_service_id) IS TRUE OR 
        (cd.origin_service_id IS NULL AND ObservationFlag.origin_service_id IS NULL)
        )
    AND cd.component_name_version = ObservationFlag.component_name_version 
	AND (
        (cd.component_purl_type = ObservationFlag.component_purl_type) IS TRUE OR 
        (cd.component_purl_type IS NULL AND ObservationFlag.component_purl_type IS NULL)
        )
;
"""

DROP_SQL = "DROP VIEW IF EXISTS core_component;"


class Migration(migrations.Migration):
    dependencies = [
        ("licenses", "0020_license_component_component_cyclonedx_bom_link"),
        ("core", "0066_alter_observation_assessment_vex_justification_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql=CREATE_SQL,
            reverse_sql=DROP_SQL,
        ),
    ]
