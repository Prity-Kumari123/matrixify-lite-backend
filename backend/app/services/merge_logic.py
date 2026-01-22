def merge_dict(existing, incoming):
    for key, value in incoming.items():
        if value is not None:
            existing[key] = value
    return existing
