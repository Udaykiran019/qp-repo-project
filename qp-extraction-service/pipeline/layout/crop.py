import os
import cv2

CROPPABLE_LABELS = {"image", "table"}

def save_element_crops(image_path: str, elements: list, document_id: str, page_number: int, storage_path: str) -> list:
    img = cv2.imread(image_path)
    out_dir = os.path.join(storage_path, "crops", document_id)
    os.makedirs(out_dir, exist_ok=True)

    for element in elements:
        if element["label"] not in CROPPABLE_LABELS or not element["bbox"]:
            continue
        x1, y1, x2, y2 = element["bbox"]
        crop = img[y1:y2, x1:x2]
        filename = f"page_{page_number}_idx_{element['index']}_{element['label']}.png"
        path = os.path.join(out_dir, filename)
        cv2.imwrite(path, crop)
        element["crop_path"] = path

    return elements