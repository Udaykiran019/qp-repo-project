# test_table_validator.py  (temporary, delete once confirmed working)
from pipeline.validation.table_validator import validate_table

wages_table_html = '''<html><body><table><tr><td>wages</td><td>100</td><td>1OI</td><td>102</td><td>100</td><td>66</td><td>97</td><td>98</td><td>96</td><td>95</td><td>102</td></tr><tr><td>Cost of living</td><td>98</td><td>66</td><td>99</td><td>95</td><td>92</td><td>95</td><td>94</td><td>90</td><td>91</td><td>97</td></tr></table></body></html>'''

probability_table_html = '''<html><body><table><tr><td>X</td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><td>P(x)</td><td>0</td><td>K</td><td>2K</td><td>2K</td><td>3K</td><td>$K^{}$</td><td>$2K^{}$</td><td>下 $\\overline{{7\\mathrm{K}^{2}+\\mathrm{K}}}$</td></tr></table></body></html>'''

clean_table_html = '''<html><body><table><tr><td>Before</td><td>45</td><td>73</td><td>46</td><td>124</td></tr><tr><td>After</td><td>36</td><td>09</td><td>44</td><td>119</td></tr></table></body></html>'''

for name, html in [("wages (has 1OI)", wages_table_html),
                    ("probability (has 添/下)", probability_table_html),
                    ("clean table", clean_table_html)]:
    print(f"\n=== {name} ===")
    result = validate_table(html)
    print(f"needs_review: {result['needs_review']}")
    for f in result["flags"]:
        print(f"  row {f['row']}, col {f['col']}: '{f['value']}' -> {f['reason']}"
              f"{' (suggested: ' + f['suggested'] + ')' if f['suggested'] else ''} [{f['severity']}]")