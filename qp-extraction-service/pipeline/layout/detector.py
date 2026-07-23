from paddleocr import PPStructureV3

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = PPStructureV3(device="cpu")
    return _engine

def detect_regions(image_path: str) -> list:
    engine = get_engine()
    result = engine.predict(image_path)

    regions = []
    for idx, block in enumerate(result[0]["layout_det_res"]["boxes"]):
        regions.append({
            "id": idx,
            "type": block["label"],
            "bbox": [int(v) for v in block["coordinate"]],
            "confidence": round(float(block["score"]), 3)
        })
    return regions