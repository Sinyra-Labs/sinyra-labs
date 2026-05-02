"""Feature classifier: is this a real product/feature launch?"""

from sinyra.normalize.schema import ClassifiedFeature, RawItem


def classify(item: RawItem) -> ClassifiedFeature:
    # TODO(P4): load prompt from sinyra/intelligence/prompts/classify.{version}.md
    # TODO(P4): call openai_client.chat_json with response_format=json_object
    # TODO(P4): parse response with ClassifiedFeature.model_validate_json
    raise NotImplementedError
