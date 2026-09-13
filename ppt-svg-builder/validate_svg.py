"""PPT SVG Builder — Safety Rule Validator

Validates an SVG file against the 6 safety rules defined in ppt-svg-builder skill.
Usage: python validate_svg.py <path-to-svg>
"""

import sys
import re
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"

def load_svg(path):
    ET.register_namespace('', SVG_NS)
    tree = ET.parse(path)
    root = tree.getroot()
    return tree, root

def rule1_all_tspan(root):
    """Rule 1: Every <text> must use ONLY <tspan> children, no bare text nodes."""
    violations = []
    for text_elem in root.iter(f"{{{SVG_NS}}}text"):
        has_tspan = False
        has_direct_text = False
        direct_samples = []
        for child in text_elem:
            if child.tag == f"{{{SVG_NS}}}tspan":
                has_tspan = True
            else:
                pass
        # Check for bare text: ET represents text between tags as `text` and `tail`
        if text_elem.text and text_elem.text.strip():
            has_direct_text = True
            direct_samples.append(text_elem.text.strip()[:50])
        if has_direct_text:
            violations.append({
                "element": ET.tostring(text_elem, encoding='unicode')[:120],
                "direct_text": direct_samples
            })
    return violations

def rule2_no_fullwidth_leading(root):
    """Rule 2: No U+3000 (fullwidth space) as first character of any tspan."""
    violations = []
    for tspan in root.iter(f"{{{SVG_NS}}}tspan"):
        text = tspan.text or ""
        if text and text[0] == '\u3000':
            violations.append({
                "tspan_text": repr(text[:50]),
                "parent": ET.tostring(list(root.iter(f"{{{SVG_NS}}}text"))[0], encoding='unicode')[:100]
                    if list(root.iter(f"{{{SVG_NS}}}text")) else "N/A"
            })
    return violations

def rule3_semantic_breaks(root):
    """Rule 3: Line breaks must NOT split words mid-character (Chinese specific).
    
    For Chinese text, check that each tspan doesn't end mid-word.
    A "mid-word" break in Chinese is harder to define algorithmically,
    so this checks for obvious violations: a tspan ending with an opening
    bracket or starting with a closing bracket/punctuation that belongs to prev line.
    """
    violations = []
    all_tspans = list(root.iter(f"{{{SVG_NS}}}tspan"))
    for i, tspan in enumerate(all_tspans):
        text = (tspan.text or "").strip()
        if not text:
            continue
        # Check: starts with mid-sentence punctuation that belongs to previous line
        if text[0] in '，。、；：）】》％':
            # This is probably OK if it's the start of a new sentence
            # Flag only if it's clearly a continuation character
            if text[0] in '，、；：':
                violations.append({
                    "issue": "tspan starts with mid-sentence punctuation",
                    "text": text[:50],
                    "position": i
                })
    # Check for YAML-like issue: single char trailing on line
    # This is a heuristic — real validation needs human review
    return violations

def rule4_line_width(root):
    """Rule 4: Estimate line width for Chinese text and flag potential overflows.
    
    Chinese char ≈ font-size px, digit ≈ font-size × 0.55 px.
    """
    warnings = []
    # Find all text elements, get their x and font-size
    for text_elem in root.iter(f"{{{SVG_NS}}}text"):
        x = text_elem.get('x')
        font_size_str = text_elem.get('font-size', '15')
        if not x:
            continue
        try:
            x_val = float(x)
            fs = float(font_size_str.replace('px', ''))
        except (ValueError, TypeError):
            continue
        
        for tspan in text_elem.iter(f"{{{SVG_NS}}}tspan"):
            text = tspan.text or ""
            if not text.strip():
                continue
            # Estimate width
            width = 0
            for ch in text:
                if '\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f':
                    width += fs  # CJK char
                elif ch.isdigit():
                    width += fs * 0.55
                elif ch in '，。、；：！？（）【】《》""''…—·%‰':
                    width += fs * 0.5
                else:
                    width += fs * 0.6
            
            # Find parent container width (simplified: canvas right edge = 1800)
            # Available width from x position to right edge
            max_width = 1800 - x_val
            if max_width <= 0:
                continue  # skip right-aligned elements (page numbers, etc.)
            
            if width > max_width * 0.95:  # 95% threshold
                warnings.append({
                    "text": text[:60],
                    "estimated_width": round(width, 1),
                    "max_width": round(max_width, 1),
                    "overflow_pct": round((width / max_width - 1) * 100, 1)
                })
    return warnings

def rule5_image_aspect(root):
    """Rule 5: Image frames must not hardcode mismatched aspect ratios.
    
    Check: if an image has explicit width/height, flag if ratio is suspicious (e.g., 4:3 in 16:9).
    This is a heuristic — real validation needs to compare with source image.
    """
    warnings = []
    for image in root.iter(f"{{{SVG_NS}}}image"):
        w = image.get('width')
        h = image.get('height')
        if w and h:
            try:
                w_val = float(w)
                h_val = float(h)
                ratio = w_val / h_val
                # Flag if ratio is close to 4:3 (1.33) or 1:1 — likely needs checking
                if 1.2 < ratio < 1.45:
                    warnings.append({
                        "ratio": round(ratio, 2),
                        "note": "Close to 4:3 — verify source image is also 4:3"
                    })
                elif 0.9 < ratio < 1.1:
                    warnings.append({
                        "ratio": round(ratio, 2),
                        "note": "Close to 1:1 — verify source image is square"
                    })
            except (ValueError, TypeError):
                pass
    return warnings

def rule6_no_g_clippath_image(root):
    """Rule 6: No <g clip-path> wrapping <image>."""
    violations = []
    for g in root.iter(f"{{{SVG_NS}}}g"):
        clip = g.get('clip-path')
        if clip:
            for image in g.iter(f"{{{SVG_NS}}}image"):
                violations.append({
                    "clip_path": clip,
                    "image_href": image.get('href', image.get('{http://www.w3.org/1999/xlink}href', 'N/A'))[:80]
                })
    return violations

def check_size_ladder(root):
    """Bonus: Check all font-sizes on page form a single ladder."""
    sizes = set()
    for elem in root.iter():
        fs = elem.get('font-size')
        if fs:
            try:
                sizes.add(float(fs.replace('px', '')))
            except ValueError:
                pass
    # Check if sizes fit one of the defined ladders
    standard = {22, 18, 15, 12, 14, 11}
    if sizes and not sizes.issubset(standard):
        return list(sizes)
    return None

def check_action_title(root):
    """Bonus: Title should be a conclusion, not a topic label."""
    # Find the main title (first text element in header area, y < 200)
    for text_elem in root.iter(f"{{{SVG_NS}}}text"):
        y = text_elem.get('y')
        if y and float(y) < 200 and float(y) > 100:
            for tspan in text_elem.iter(f"{{{SVG_NS}}}tspan"):
                title = (tspan.text or "").strip()
                if title:
                    # Heuristic: topic labels are short, conclusions are longer with data
                    if len(title) < 6:
                        return f"Title too short, likely topic label: '{title}'"
                    return None  # Looks OK
    return "No title found in header area"

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_svg.py <path-to-svg>")
        sys.exit(1)
    
    path = sys.argv[1]
    print(f"=== PPT SVG Safety Validator ===\n")
    print(f"File: {path}\n")
    
    tree, root = load_svg(path)
    
    all_pass = True
    total_checks = 0
    passed_checks = 0
    
    # Rule 1
    total_checks += 1
    v1 = rule1_all_tspan(root)
    if v1:
        print(f"❌ Rule 1 (all-tspan): FAILED — {len(v1)} violation(s)")
        for v in v1:
            print(f"   Direct text found: {v['direct_text']}")
        all_pass = False
    else:
        print(f"✅ Rule 1 (all-tspan): PASSED")
        passed_checks += 1
    
    # Rule 2
    total_checks += 1
    v2 = rule2_no_fullwidth_leading(root)
    if v2:
        print(f"❌ Rule 2 (no U+3000 leading): FAILED — {len(v2)} violation(s)")
        all_pass = False
    else:
        print(f"✅ Rule 2 (no U+3000 leading): PASSED")
        passed_checks += 1
    
    # Rule 3
    total_checks += 1
    v3 = rule3_semantic_breaks(root)
    if v3:
        print(f"⚠️  Rule 3 (semantic breaks): {len(v3)} warning(s) — needs human review")
        for v in v3:
            print(f"   {v}")
    else:
        print(f"✅ Rule 3 (semantic breaks): PASSED (heuristic only)")
        passed_checks += 1
    
    # Rule 4
    total_checks += 1
    v4 = rule4_line_width(root)
    if v4:
        print(f"⚠️  Rule 4 (line width): {len(v4)} potential overflow(s)")
        for v in v4:
            print(f"   '{v['text']}' — est {v['estimated_width']}px / max {v['max_width']}px ({v['overflow_pct']}% over)")
    else:
        print(f"✅ Rule 4 (line width): PASSED")
        passed_checks += 1
    
    # Rule 5
    total_checks += 1
    v5 = rule5_image_aspect(root)
    if v5:
        print(f"⚠️  Rule 5 (image aspect): {len(v5)} warning(s)")
        for v in v5:
            print(f"   Ratio {v['ratio']} — {v['note']}")
    else:
        print(f"✅ Rule 5 (image aspect): N/A (no images)")
        passed_checks += 1
    
    # Rule 6
    total_checks += 1
    v6 = rule6_no_g_clippath_image(root)
    if v6:
        print(f"❌ Rule 6 (no g/clipPath on image): FAILED — {len(v6)} violation(s)")
        all_pass = False
    else:
        print(f"✅ Rule 6 (no g/clipPath on image): PASSED")
        passed_checks += 1
    
    # Bonus: size ladder
    sizes = check_size_ladder(root)
    if sizes:
        print(f"\n⚠️  Size ladder: non-standard sizes found — {sizes}")
        print(f"   Standard ladders: 22/18/15/14/12/11 (standard), 28/18/14 (impact), 20/16/14/11 (dense)")
    else:
        print(f"\n✅ Size ladder: all font-sizes within standard ladders")
        passed_checks += 1
    
    # Bonus: action title
    title_issue = check_action_title(root)
    if title_issue:
        print(f"⚠️  Action title: {title_issue}")
    else:
        print(f"✅ Action title: appears to be a conclusion statement")
        passed_checks += 1
    
    total_checks = 8  # 6 rules + 2 bonuses
    print(f"\n{'='*40}")
    print(f"Result: {passed_checks}/{total_checks} checks passed")
    
    if all_pass:
        print("✅ ALL SAFETY RULES PASSED — SVG is safe for PPTX export")
        sys.exit(0)
    else:
        print("❌ SAFETY VIOLATIONS FOUND — fix before exporting to PPTX")
        sys.exit(1)

if __name__ == "__main__":
    main()