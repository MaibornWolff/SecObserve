import re

from application.core.models import Product, Parser, Observation
from application.core.services.observation import (
    get_current_severity,
    get_current_status,
)
from application.core.services.observation_log import create_observation_log
from application.rules.models import Rule


class Rule_Engine:
    def __init__(self, product: Product, parser: Parser):
        product_parser_rules = Rule.objects.filter(
            product=product, parser=parser, enabled=True
        )
        self.rules: list[Rule] = list(product_parser_rules)

        if product.apply_general_rules:
            parser_rules = Rule.objects.filter(
                product__isnull=True, parser=parser, enabled=True
            )
            self.rules += list(parser_rules)

        self.product = product
        self.parser = parser

    def apply_rules_for_observation(self, observation: Observation) -> None:
        previous_product_rule = None
        if observation.product_rule:
            previous_product_rule = observation.product_rule
        previous_general_rule = None
        if observation.general_rule:
            previous_general_rule = observation.general_rule
        observation.product_rule = None
        observation.general_rule = None

        rule_found = False
        for rule in self.rules:
            if (
                observation.parser == rule.parser
                and (
                    not rule.scanner_prefix
                    or observation.scanner.lower().startswith(
                        rule.scanner_prefix.lower()
                    )
                )
                and self._check_regex(rule.title, observation.title)
                and self._check_regex(
                    rule.origin_component_name_version,
                    observation.origin_component_name_version,
                )
                and self._check_regex(
                    rule.origin_docker_image_name_tag,
                    observation.origin_docker_image_name_tag,
                )
                and self._check_regex(
                    rule.origin_endpoint_url, observation.origin_endpoint_url
                )
                and self._check_regex(
                    rule.origin_service_name, observation.origin_service_name
                )
                and self._check_regex(
                    rule.origin_source_file, observation.origin_source_file
                )
            ):
                previous_severity = observation.current_severity
                previous_rule_severity = observation.rule_severity
                if rule.new_severity:
                    observation.rule_severity = rule.new_severity
                    observation.current_severity = get_current_severity(observation)

                previous_status = observation.current_status
                previous_rule_status = observation.rule_status
                if rule.new_status:
                    observation.rule_status = rule.new_status
                    observation.current_status = get_current_status(observation)

                if rule.product:
                    observation.product_rule = rule
                else:
                    observation.general_rule = rule

                # Write observation and observation log if status or severity has been changed
                if (
                    previous_rule_status != observation.rule_status
                    or previous_rule_severity != observation.rule_severity
                    or previous_status != observation.current_status
                    or previous_severity != observation.current_severity
                    or previous_general_rule != observation.general_rule
                    or previous_product_rule != observation.product_rule
                ):
                    if previous_status != observation.current_status:
                        status = observation.current_status
                    else:
                        status = ""
                    if previous_severity != observation.current_severity:
                        severity = observation.current_severity
                    else:
                        severity = ""

                    if rule.product:
                        comment = f"Updated by product rule {rule.name}"
                    else:
                        comment = f"Updated by general rule {rule.name}"

                    create_observation_log(observation, severity, status, comment)

                rule_found = True
                break

        if not rule_found and (
            previous_general_rule != observation.general_rule
            or previous_product_rule != observation.product_rule
        ):
            observation.rule_severity = ""
            previous_severity = observation.current_severity
            observation.current_severity = get_current_severity(observation)
            observation.rule_status = ""
            previous_status = observation.current_status
            observation.current_status = get_current_status(observation)

            if previous_status != observation.current_status:
                status = observation.current_status
            else:
                status = ""
            if previous_severity != observation.current_severity:
                severity = observation.current_severity
            else:
                severity = ""

            if previous_product_rule:
                comment = f"Removed product rule {previous_product_rule.name}"
            else:
                comment = f"Removed general rule {previous_general_rule.name}"

            create_observation_log(observation, severity, status, comment)

    def apply_all_rules_for_product_and_parser(self) -> None:
        for observation in Observation.objects.filter(
            product=self.product, parser=self.parser
        ):
            self.apply_rules_for_observation(observation)

    def _check_regex(self, pattern: str, value: str) -> bool:
        if not pattern:
            return True

        if not value:
            return False

        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        return compiled_pattern.match(value) is not None
