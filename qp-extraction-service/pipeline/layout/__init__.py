import os
import json
from .detector import run_detection
from .parser import extract_elements
from .crop import save_element_crops

def run_layout_detection(pages: list, document_id: str, storage_path: str) -> list:
    results = []
    layout_dir = os.path.join(storage_path, "layout", document_id)
    os.makedirs(layout_dir, exist_ok=True)

    for page in pages:
        raw_result = run_detection(page["image_path"])
        elements = extract_elements(raw_result)
        elements = save_element_crops(page["image_path"], elements, document_id, page["page_number"], storage_path)

        page_result = {"page_number": page["page_number"], "elements": elements}
        results.append(page_result)

        with open(os.path.join(layout_dir, f"page_{page['page_number']}.json"), "w") as f:
            json.dump(page_result, f, indent=2)

    return results