# secobserve

![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.38.0](https://img.shields.io/badge/AppVersion-1.38.0-informational?style=flat-square)

A Helm chart to deploy SecObserve, an open-source vulnerability and license management system designed for software development teams and cloud-native environments. SecObserve helps teams identify, manage, and remediate security vulnerabilities and license compliance issues across their software projects, enhancing visibility and improving DevSecOps workflows.

**Homepage:** <https://github.com/MaibornWolff/SecObserve>

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| SecObserve community |  |  |

## Source Code

* <https://github.com/MaibornWolff/SecObserve>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://registry-1.docker.io/bitnamicharts | postgresql | 16.x.x |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| backend.env[0].name | string | `"ADMIN_USER"` |  |
| backend.env[0].value | string | `"admin"` |  |
| backend.env[10].name | string | `"CORS_ALLOWED_ORIGINS"` |  |
| backend.env[10].value | string | `"https://secobserve.dev"` |  |
| backend.env[11].name | string | `"DJANGO_SECRET_KEY"` |  |
| backend.env[11].valueFrom.secretKeyRef.key | string | `"django_secret_key"` |  |
| backend.env[11].valueFrom.secretKeyRef.name | string | `"secobserve-secrets"` |  |
| backend.env[12].name | string | `"FIELD_ENCRYPTION_KEY"` |  |
| backend.env[12].valueFrom.secretKeyRef.key | string | `"field_encryption_key"` |  |
| backend.env[12].valueFrom.secretKeyRef.name | string | `"secobserve-secrets"` |  |
| backend.env[13].name | string | `"OIDC_AUTHORITY"` |  |
| backend.env[13].value | string | `"https://oidc.secobserve.dev"` |  |
| backend.env[14].name | string | `"OIDC_CLIENT_ID"` |  |
| backend.env[14].value | string | `"secobserve"` |  |
| backend.env[15].name | string | `"OIDC_USERNAME"` |  |
| backend.env[15].value | string | `"preferred_username"` |  |
| backend.env[16].name | string | `"OIDC_FIRST_NAME"` |  |
| backend.env[16].value | string | `"given_name"` |  |
| backend.env[17].name | string | `"OIDC_LAST_NAME"` |  |
| backend.env[17].value | string | `"family_name"` |  |
| backend.env[18].name | string | `"OIDC_FULL_NAME"` |  |
| backend.env[18].value | string | `"preferred_username"` |  |
| backend.env[19].name | string | `"OIDC_EMAIL"` |  |
| backend.env[19].value | string | `"email"` |  |
| backend.env[1].name | string | `"ADMIN_PASSWORD"` |  |
| backend.env[1].valueFrom.secretKeyRef.key | string | `"password"` |  |
| backend.env[1].valueFrom.secretKeyRef.name | string | `"secobserve-secrets"` |  |
| backend.env[20].name | string | `"OIDC_GROUPS"` |  |
| backend.env[20].value | string | `"groups"` |  |
| backend.env[2].name | string | `"ADMIN_EMAIL"` |  |
| backend.env[2].value | string | `"admin@admin.com"` |  |
| backend.env[3].name | string | `"DATABASE_ENGINE"` |  |
| backend.env[3].value | string | `"django.db.backends.postgresql"` |  |
| backend.env[4].name | string | `"DATABASE_HOST"` |  |
| backend.env[4].value | string | `"release-name-postgresql"` |  |
| backend.env[5].name | string | `"DATABASE_PORT"` |  |
| backend.env[5].value | string | `"5432"` |  |
| backend.env[6].name | string | `"DATABASE_DB"` |  |
| backend.env[6].value | string | `"secobserve"` |  |
| backend.env[7].name | string | `"DATABASE_USER"` |  |
| backend.env[7].value | string | `"secobserve"` |  |
| backend.env[8].name | string | `"DATABASE_PASSWORD"` |  |
| backend.env[8].valueFrom.secretKeyRef.key | string | `"password"` |  |
| backend.env[8].valueFrom.secretKeyRef.name | string | `"release-name-postgresql"` |  |
| backend.env[9].name | string | `"ALLOWED_HOSTS"` |  |
| backend.env[9].value | string | `"*"` |  |
| backend.image.pullPolicy | string | `"IfNotPresent"` |  |
| backend.image.registry | string | `"docker.io"` |  |
| backend.image.repository | string | `"maibornwolff/secobserve-backend"` |  |
| backend.image.tag | string | `"1.30.1"` |  |
| backend.resources.limits.cpu | string | `"1000m"` |  |
| backend.resources.limits.memory | string | `"1500Mi"` |  |
| backend.resources.requests.cpu | string | `"1000m"` |  |
| backend.resources.requests.memory | string | `"1500Mi"` |  |
| backend.service.port | int | `5000` |  |
| dbchecker.enabled | bool | `true` |  |
| dbchecker.hostname | string | `"release-name-postgresql"` |  |
| dbchecker.image.pullPolicy | string | `"IfNotPresent"` |  |
| dbchecker.image.repository | string | `"busybox"` |  |
| dbchecker.image.tag | string | `"latest"` |  |
| dbchecker.port | int | `5432` |  |
| dbchecker.resources.limits.cpu | string | `"20m"` |  |
| dbchecker.resources.limits.memory | string | `"32Mi"` |  |
| dbchecker.resources.requests.cpu | string | `"20m"` |  |
| dbchecker.resources.requests.memory | string | `"32Mi"` |  |
| dbchecker.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| dbchecker.securityContext.runAsGroup | int | `1000` |  |
| dbchecker.securityContext.runAsNonRoot | bool | `true` |  |
| dbchecker.securityContext.runAsUser | int | `1000` |  |
| frontend.env[0].name | string | `"API_BASE_URL"` |  |
| frontend.env[0].value | string | `"https://secobserve.dev/api"` |  |
| frontend.env[1].name | string | `"OIDC_ENABLED"` |  |
| frontend.env[1].value | string | `"true"` |  |
| frontend.env[2].name | string | `"OIDC_AUTHORITY"` |  |
| frontend.env[2].value | string | `"https://oidc.secobserve.dev"` |  |
| frontend.env[3].name | string | `"OIDC_CLIENT_ID"` |  |
| frontend.env[3].value | string | `"secobserve"` |  |
| frontend.env[4].name | string | `"OIDC_REDIRECT_URI"` |  |
| frontend.env[4].value | string | `"https://secobserve.dev/"` |  |
| frontend.env[5].name | string | `"OIDC_POST_LOGOUT_REDIRECT_URI"` |  |
| frontend.env[5].value | string | `"https://secobserve.dev/"` |  |
| frontend.image.pullPolicy | string | `"IfNotPresent"` |  |
| frontend.image.registry | string | `"docker.io"` |  |
| frontend.image.repository | string | `"maibornwolff/secobserve-frontend"` |  |
| frontend.image.tag | string | `"1.30.1"` |  |
| frontend.resources.limits.cpu | string | `"500m"` |  |
| frontend.resources.limits.memory | string | `"1000Mi"` |  |
| frontend.resources.requests.cpu | string | `"500m"` |  |
| frontend.resources.requests.memory | string | `"1000Mi"` |  |
| frontend.service.port | int | `3000` |  |
| ingress.annotations."alb.ingress.kubernetes.io/healthcheck-path" | string | `"/"` |  |
| ingress.annotations."alb.ingress.kubernetes.io/listen-ports" | string | `"[{\"HTTPS\": 443}]"` |  |
| ingress.annotations."alb.ingress.kubernetes.io/ssl-policy" | string | `"ELBSecurityPolicy-TLS13-1-2-FIPS-2023-04"` |  |
| ingress.enabled | bool | `true` |  |
| ingress.hostname | string | `"secobserve.dev"` |  |
| ingress.ingressClassName | string | `"alb"` |  |
| nodeSelector | object | `{}` |  |
| postgresql.architecture | string | `"standalone"` |  |
| postgresql.auth.database | string | `"secobserve"` |  |
| postgresql.auth.existingSecret | string | `""` |  |
| postgresql.auth.password | string | `""` |  |
| postgresql.auth.postgresPassword | string | `""` |  |
| postgresql.auth.secretKeys.userPasswordKey | string | `"password"` |  |
| postgresql.auth.username | string | `"secobserve"` |  |
| postgresql.enabled | bool | `true` |  |
| replicaCount | int | `1` |  |
| service.type | string | `"NodePort"` |  |
| tolerations | object | `{}` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)
