#!/bin/sh

rm sbom_backend_application_1.7.0.json
rm sbom_frontend_application_1.7.0.json
rm sbom_backend_container_1.7.0.json
rm sbom_frontend_container_1.7.0.json

echo "Generating backend application SBOM ..."
echo
cyclonedx-py poetry --only main,prod --output-format json ../backend \
  | sbom-utility patch --patch-file ./configuration/patch_1.4.json --quiet --input-file - \
  | parlay ecosystems enrich - \
  | sbom-utility patch --patch-file ./configuration/patch_1.5.json --quiet --input-file - \
  | sbom-utility trim --keys=externalReferences,properties,vulnerabilities --quiet --input-file - \
  | sbom-utility patch --patch-file ./configuration/patch_backend_application.json --quiet --input-file - --output-file sbom_backend_application_1.7.0.json
sbom-utility validate --input-file sbom_backend_application_1.7.0.json

echo
echo "Generating frontend application SBOM ..."
echo
cyclonedx-npm --omit dev --package-lock-only --output-format JSON ../frontend/package-lock.json \
  | sbom-utility patch --patch-file ./configuration/patch_1.4.json --quiet --input-file - \
  | parlay ecosystems enrich - \
  | sbom-utility patch --patch-file ./configuration/patch_1.5.json --quiet --input-file - \
  | sbom-utility trim --keys=externalReferences,properties,vulnerabilities --quiet --input-file - \
  | sbom-utility patch --patch-file ./configuration/patch_frontend_application.json --quiet --input-file - --output-file sbom_frontend_application_1.7.0.json
sbom-utility validate --input-file sbom_frontend_application_1.7.0.json

echo
echo "Generating backend container SBOM ..."
echo
trivy image --vuln-type os --scanners license --format cyclonedx --quiet maibornwolff/secobserve-backend:1.7.0 \
  | sbom-utility trim --keys=externalReferences,properties,vulnerabilities --quiet --input-file - \
  | sbom-utility patch --patch-file ./configuration/patch_backend_container.json --quiet --input-file - --output-file sbom_backend_container_1.7.0.json
sbom-utility validate --input-file sbom_backend_container_1.7.0.json

echo
echo "Generating frontend container SBOM ..."
echo
trivy image --vuln-type os --scanners license --format cyclonedx maibornwolff/secobserve-frontend:1.7.0 \
  | sbom-utility trim --keys=externalReferences,properties,vulnerabilities --quiet --input-file - \
  | sbom-utility patch --patch-file ./configuration/patch_frontend_container.json --quiet --input-file - --output-file sbom_frontend_container_1.7.0.json
sbom-utility validate --input-file sbom_frontend_container_1.7.0.json
