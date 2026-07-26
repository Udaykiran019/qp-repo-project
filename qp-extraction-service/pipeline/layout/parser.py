def _get(obj, key, default=None):
    try:
        return obj[key]
    except (TypeError, KeyError):
        return getattr(obj, key, default)

def extract_elements(result) -> list:
    parsing_blocks = result.get("parsing_res_list", []) if hasattr(result, "get") else result["parsing_res_list"]

    elements = []
    for block in parsing_blocks:
        bbox = _get(block, "bbox", [])
        elements.append({
            "index": _get(block, "index"),
            "order_index": _get(block, "order_index"),
            "label": _get(block, "label"),
            "order_label": _get(block, "order_label"),
            "content": _get(block, "content"),
            "bbox": [int(v) for v in bbox] if bbox else [],
        })

    # Sort by order_index, pushing None (out-of-flow: images, tables, footers, page numbers) to the end
    elements.sort(key=lambda e: (e["order_index"] is None, e["order_index"] or 0))
    return elements