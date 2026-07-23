import os
import cv2

def save_region_crops(image_path: str, regions: list, document_id: str, page_number: int, storage_path: str) -> list:
    img = cv2.imread(image_path)
    out_dir = os.path.join(storage_path, "crops", document_id)
    os.makedirs(out_dir, exist_ok=True)

    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        crop = img[y1:y2, x1:x2]
        filename = f"page_{page_number}_region_{region['id']}_{region['type']}.png"
        path = os.path.join(out_dir, filename)
        cv2.imwrite(path, crop)
        region["crop_path"] = path

    return regions