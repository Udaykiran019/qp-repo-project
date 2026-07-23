def classify_page(pdf_page) -> str:
    text = pdf_page.get_text().strip()
    return "digital" if len(text) > 40 else "scanned"