import os
import fitz
import numpy as np

def pixmap_to_ndarray(pix: fitz.Pixmap) -> np.ndarray:
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    return img

def save_page_image(img: np.ndarray, document_id: str, page_number: int, storage_path: str) -> str:
    import cv2
    out_dir = os.path.join(storage_path, "pages", document_id)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"page_{page_number}.png")
    cv2.imwrite(out_path, img)
    return out_path