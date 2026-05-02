"""Hash-based deduplication against seen-items store."""

# TODO(P3): implement compute_hash(item: RawItem) -> str  (md5 of title + "|" + link)
# TODO(P3): implement filter_seen(items: list[RawItem], store: SeenStore) -> tuple[list[RawItem], dict[str, int]]
