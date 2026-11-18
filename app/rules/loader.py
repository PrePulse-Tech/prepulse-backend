import json
import logging
from collections.abc import Iterable, Mapping
from typing import Any, Protocol

from app.rules.base import Rule, RuleConfig

logger = logging.getLogger(__name__)


class RuleRepository(Protocol):
    """Where the rules come from. The database implements this later."""

    def fetch_rules(self) -> Iterable[Mapping[str, Any]]:
        """Return rows shaped like the detection_rule table."""


def load_rules(
    repository: RuleRepository, registry: Mapping[str, type[Rule]]
) -> list[Rule]:
    """Build rule objects from the stored rules.

    `registry` maps a failure_type (for example "php_error") to the Rule class
    that handles it. Disabled rules are skipped, and so are rules whose
    failure_type has no class, so one bad row does not stop the others.
    """
    rules: list[Rule] = []
    for record in repository.fetch_rules():
        data = dict(record)
        raw_config = data.get("config")
        if raw_config is None:
            data["config"] = {}
        elif isinstance(raw_config, str):
            data["config"] = json.loads(raw_config) if raw_config.strip() else {}
        config = RuleConfig.model_validate(data)
        if not config.enabled:
            continue
        rule_class = registry.get(config.failure_type)
        if rule_class is None:
            logger.warning(
                "No rule class for failure_type %r (rule %s), skipping",
                config.failure_type,
                config.rule_id,
            )
            continue
        rules.append(rule_class(config))
    return rules
