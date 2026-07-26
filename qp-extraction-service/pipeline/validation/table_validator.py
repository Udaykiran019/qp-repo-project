# pipeline/validation/table_validator.py
import re
from bs4 import BeautifulSoup

NUMERIC_PATTERN = re.compile(r'^-?\d+(\.\d+)?%?$')
SYMBOLIC_PATTERN = re.compile(r'^\$?\d*[A-Za-z](\^\{?\d*\}?)?\$?$')
NON_LATIN_PATTERN = re.compile(r'[^\x00-\x7F°%.\-]')

CONFUSION_RULES = [
    (re.compile(r'[Oo]'), '0', 'high'),
    (re.compile(r'[Il|]'), '1', 'high'),
    (re.compile(r'[Ss]'), '5', 'medium'),
    (re.compile(r'[B]'), '8', 'medium'),
]


def parse_table_html(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    return [[td.get_text(strip=True) for td in tr.find_all(['td', 'th'])] for tr in soup.find_all('tr')]


def classify_rows(rows: list) -> dict:
    """Column 0 is always a row label. For every row, classify whether the
    REST of that row (columns 1+) is a numeric data series, based on all
    values in that row — far more reliable than per-column stats when
    tables are wide and short."""
    classification = {}
    for row_idx, row in enumerate(rows):
        values = [v for v in row[1:] if v]
        if not values:
            classification[row_idx] = 'label'
            continue
        acceptable = sum(1 for v in values if NUMERIC_PATTERN.match(v) or SYMBOLIC_PATTERN.match(v))
        classification[row_idx] = 'numeric' if (acceptable / len(values)) >= 0.5 else 'label'
    return classification


def try_fix_confusions(value: str):
    candidate = value
    applied_severities = []
    for pattern, replacement, severity in CONFUSION_RULES:
        new_candidate = pattern.sub(replacement, candidate)
        if new_candidate != candidate:
            applied_severities.append(severity)
        candidate = new_candidate

    if candidate != value and NUMERIC_PATTERN.match(candidate):
        overall_severity = 'high' if 'high' in applied_severities else 'medium'
        return candidate, overall_severity
    return None, None


def check_cell(value: str, row: int, col: int, row_type: str) -> list:
    flags = []
    if not value:
        return flags

    if NON_LATIN_PATTERN.search(value):
        flags.append({"row": row, "col": col, "value": value,
                       "reason": "non_latin_character", "suggested": None, "severity": "high"})
        return flags

    if col == 0 or row_type != 'numeric':
        return flags

    if NUMERIC_PATTERN.match(value) or SYMBOLIC_PATTERN.match(value):
        return flags

    suggested, severity = try_fix_confusions(value)
    if suggested:
        flags.append({"row": row, "col": col, "value": value,
                       "reason": "letter_digit_confusion", "suggested": suggested, "severity": severity})
    else:
        flags.append({"row": row, "col": col, "value": value,
                       "reason": "malformed_numeric", "suggested": None, "severity": "high"})
    return flags


def check_outliers(rows: list, row_types: dict) -> list:
    flags = []
    for row_idx, row_type in row_types.items():
        if row_type != 'numeric':
            continue
        row = rows[row_idx]
        digit_counts = [(c, len(re.sub(r'\D', '', row[c]))) for c in range(1, len(row))
                         if row[c] and re.sub(r'\D', '', row[c])]
        if len(digit_counts) < 3:
            continue
        lengths = [c for _, c in digit_counts]
        mode_len = max(set(lengths), key=lengths.count)
        for col, length in digit_counts:
            if abs(length - mode_len) >= 2:
                flags.append({"row": row_idx, "col": col, "value": row[col],
                               "reason": "digit_count_outlier", "suggested": None, "severity": "low"})
    return flags


def validate_table(html: str) -> dict:
    rows = parse_table_html(html)
    row_types = classify_rows(rows)

    flags = []
    for row_idx, row in enumerate(rows):
        for col_idx, value in enumerate(row):
            flags.extend(check_cell(value, row_idx, col_idx, row_types.get(row_idx, 'label')))

    flags.extend(check_outliers(rows, row_types))

    high_or_medium = [f for f in flags if f["severity"] in ("high", "medium")]
    return {"needs_review": len(high_or_medium) > 0, "flags": flags}