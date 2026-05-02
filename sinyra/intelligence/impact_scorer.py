"""Impact scorer: 0-100 impact score for classified features."""

from sinyra.normalize.schema import ClassifiedFeature, ImpactResult


def score(feature: ClassifiedFeature) -> ImpactResult:
    # TODO(P4): load prompt from sinyra/intelligence/prompts/impact.{version}.md
    # TODO(P4): call openai_client.chat_json
    # TODO(P4): parse response with ImpactResult.model_validate_json
    raise NotImplementedError
