import fitz
from .classify_page import classify_page
from .rasterize import rasterize_page
from .cleanup import clean_scanned_page
from utils.image_io import pixmap_to_ndarray, save_page_image

def preprocess_document(pdf_path: str, document_id: str, storage_path: str, dpi: int = 300):
    doc = fitz.open(pdf_path)
    pages = []
    for i in range(len(doc)):
        page_type = classify_page(doc[i])
        pix = rasterize_page(doc, i, dpi=dpi)
        img = pixmap_to_ndarray(pix)
        if page_type == "scanned":
            img = clean_scanned_page(img)
        path = save_page_image(img, document_id, i + 1, storage_path)
        pages.append({"page_number": i + 1, "type": page_type, "image_path": path, "dpi": dpi})
    return pages