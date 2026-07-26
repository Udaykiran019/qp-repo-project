# debug_inspect.py  (in qp-extraction-service/, same level as main.py)
import os
import json
from paddleocr import PPStructureV3

engine = PPStructureV3(device="cpu")

# Reuse the same page you tested before
image_path = r"C:\qp-repo-project\qp-extractor\storage\pages\a85496fc-b542-462a-b411-bcddfa384341\page_1.png"

result = engine.predict(image_path)
r = result[0]

out_dir = "debug_output"
os.makedirs(out_dir, exist_ok=True)

def safe_dump(obj):
    try:
        return json.dumps(obj, indent=2, default=str)
    except Exception as e:
        return f"<could not serialize: {e}>\n\nraw repr:\n{repr(obj)[:5000]}"

keys_to_inspect = [
    "parsing_res_list",
    "formula_res_list",
    "overall_ocr_res",
    "table_res_list",
    "chart_res_list",
    "region_det_res",
    "seal_res_list",
]

for key in keys_to_inspect:
    content = r.get(key, f"<key '{key}' not found>")
    text = safe_dump(content)
    path = os.path.join(out_dir, f"{key}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[{key}] -> {path}  ({len(text)} chars)")

print("\nDone. Check the debug_output/ folder.")