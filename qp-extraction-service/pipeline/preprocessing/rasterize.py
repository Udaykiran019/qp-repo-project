import fitz

def rasterize_page(doc, page_number, dpi=300):
    page = doc[page_number]
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    return page.get_pixmap(matrix=mat)