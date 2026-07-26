from paddleocr import PPStructureV3

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = PPStructureV3(device="cpu")
    return _engine

def run_detection(image_path: str):
    engine = get_engine()
    result = engine.predict(image_path)
    return result[0]  # full result object for this page