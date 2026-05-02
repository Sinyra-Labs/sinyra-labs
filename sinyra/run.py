"""Pipeline entrypoint: fetch → dedup → classify → score → synthesize → deliver."""

# TODO(P2): wire ingest.rss.fetch_all()
# TODO(P3): wire storage.memory.SeenStore for dedup
# TODO(P4): wire intelligence.classifier + impact_scorer
# TODO(P5): wire synthesis.brief + delivery.email.send


def main() -> None:
    # TODO: implement full pipeline
    raise NotImplementedError("Pipeline not yet implemented — run P2-P5 prompts first.")


if __name__ == "__main__":
    main()
