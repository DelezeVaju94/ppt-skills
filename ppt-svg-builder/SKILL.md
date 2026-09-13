---
name: "ppt-svg-builder"
description: "Build production-ready SVG pages for PPT with ready-to-copy templates, safety rules, and quality checklist. Invoke when user asks to create a PPT page, make a slide, generate SVG for presentation, or troubleshoot SVG-to-PPTX conversion issues."
---

# PPT SVG Builder

Build SVG slides that export cleanly to PPTX. Copy a template, change the text, and you're done.

## Design Spec Defaults (change these for your project)

| Token | Value |
|---|---|
| Primary color | `#1F3A5F` (deep blue) |
| Accent color | `#C8963E` (gold) |
| Card background | `#F5F3EE` (warm white) |
| Page background | `#0A1628` (dark navy) |
| Body text color | `#2D2D2D` |
| Body font-size | 15px |
| Title font-size | 22px |
| Subtitle font-size | 18px |
| Small label | 12px |
| Canvas | 1920 × 1080 |
| Font family | Microsoft YaHei, sans-serif |

## Component Templates

Each template is a complete, self-contained SVG. Replace placeholders (marked with `{{...}}`) with your content.

### 1. card-single — Single content card page

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" font-family="Microsoft YaHei, sans-serif">
  <rect width="1920" height="1080" fill="#0A1628"/>

  <!-- Header bar -->
  <rect x="120" y="80" width="1680" height="3" fill="#C8963E"/>
  <text x="120" y="160" font-size="22" font-weight="bold" fill="#FFFFFF">
    <tspan>{{PAGE_TITLE}}</tspan>
  </text>
  <text x="1800" y="160" font-size="14" fill="#C8963E" text-anchor="end">
    <tspan>{{SECTION_LABEL}}</tspan>
  </text>

  <!-- Content card -->
  <rect x="120" y="200" width="1680" height="{{CARD_HEIGHT:780}}" rx="8" fill="#F5F3EE"/>

  <!-- Card title -->
  <text x="160" y="250" font-size="20" font-weight="bold" fill="#1F3A5F">
    <tspan>{{CARD_TITLE}}</tspan>
  </text>

  <!-- Gold accent line under title -->
  <rect x="160" y="265" width="60" height="3" fill="#C8963E"/>

  <!-- Body text — copy this block for each paragraph -->
  <text x="160" y="310" font-size="15" fill="#2D2D2D">
    <tspan>{{BODY_LINE_1}}</tspan>
  </text>
  <text x="160" y="340" font-size="15" fill="#2D2D2D">
    <tspan>{{BODY_LINE_2}}</tspan>
  </text>

  <!-- Page number -->
  <text x="1800" y="1060" font-size="14" fill="#666666" text-anchor="end">
    <tspan>{{PAGE_NUM}}</tspan>
  </text>
</svg>
```

### 2. card-double — Left-right comparison card page

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" font-family="Microsoft YaHei, sans-serif">
  <rect width="1920" height="1080" fill="#0A1628"/>

  <!-- Header bar -->
  <rect x="120" y="80" width="1680" height="3" fill="#C8963E"/>
  <text x="120" y="160" font-size="22" font-weight="bold" fill="#FFFFFF">
    <tspan>{{PAGE_TITLE}}</tspan>
  </text>

  <!-- Left card -->
  <rect x="120" y="200" width="810" height="780" rx="8" fill="#F5F3EE"/>
  <rect x="120" y="200" width="810" height="6" fill="#C8963E" rx="3"/>
  <text x="160" y="260" font-size="20" font-weight="bold" fill="#1F3A5F">
    <tspan>{{LEFT_TITLE}}</tspan>
  </text>
  <text x="160" y="310" font-size="15" fill="#2D2D2D">
    <tspan>{{LEFT_LINE_1}}</tspan>
  </text>

  <!-- Right card -->
  <rect x="990" y="200" width="810" height="780" rx="8" fill="#F5F3EE"/>
  <rect x="990" y="200" width="810" height="6" fill="#C8963E" rx="3"/>
  <text x="1030" y="260" font-size="20" font-weight="bold" fill="#1F3A5F">
    <tspan>{{RIGHT_TITLE}}</tspan>
  </text>
  <text x="1030" y="310" font-size="15" fill="#2D2D2D">
    <tspan>{{RIGHT_LINE_1}}</tspan>
  </text>

  <!-- VS divider -->
  <rect x="955" y="400" width="10" height="80" rx="5" fill="#C8963E"/>
  <text x="960" y="460" font-size="18" font-weight="bold" fill="#C8963E" text-anchor="middle">
    <tspan>VS</tspan>
  </text>

  <!-- Page number -->
  <text x="1800" y="1060" font-size="14" fill="#666666" text-anchor="end">
    <tspan>{{PAGE_NUM}}</tspan>
  </text>
</svg>
```

### 3. big-number — Data highlight page

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" font-family="Microsoft YaHei, sans-serif">
  <rect width="1920" height="1080" fill="#0A1628"/>

  <!-- Header bar -->
  <rect x="120" y="80" width="1680" height="3" fill="#C8963E"/>
  <text x="120" y="160" font-size="22" font-weight="bold" fill="#FFFFFF">
    <tspan>{{PAGE_TITLE}}</tspan>
  </text>

  <!-- Big number card -->
  <rect x="360" y="240" width="1200" height="600" rx="8" fill="#F5F3EE"/>

  <!-- Big number -->
  <text x="960" y="500" font-size="96" font-weight="bold" fill="#1F3A5F" text-anchor="middle">
    <tspan>{{BIG_NUMBER}}</tspan>
  </text>

  <!-- Unit -->
  <text x="960" y="560" font-size="24" fill="#C8963E" text-anchor="middle">
    <tspan>{{UNIT}}</tspan>
  </text>

  <!-- Explanation -->
  <text x="960" y="620" font-size="15" fill="#666666" text-anchor="middle">
    <tspan>{{EXPLANATION}}</tspan>
  </text>

  <!-- Gold accent line -->
  <rect x="860" y="640" width="200" height="3" fill="#C8963E"/>

  <!-- Source -->
  <text x="960" y="700" font-size="12" fill="#AAAAAA" text-anchor="middle">
    <tspan>{{SOURCE}}</tspan>
  </text>

  <!-- Page number -->
  <text x="1800" y="1060" font-size="14" fill="#666666" text-anchor="end">
    <tspan>{{PAGE_NUM}}</tspan>
  </text>
</svg>
```

### 4. timeline — Timeline / axis node page

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" font-family="Microsoft YaHei, sans-serif">
  <rect width="1920" height="1080" fill="#0A1628"/>

  <!-- Header bar -->
  <rect x="120" y="80" width="1680" height="3" fill="#C8963E"/>
  <text x="120" y="160" font-size="22" font-weight="bold" fill="#FFFFFF">
    <tspan>{{PAGE_TITLE}}</tspan>
  </text>

  <!-- Timeline axis -->
  <rect x="120" y="540" width="1680" height="2" fill="rgba(200,150,62,0.3)"/>

  <!-- Node 1 -->
  <circle cx="360" cy="540" r="10" fill="#C8963E"/>
  <circle cx="360" cy="540" r="18" fill="none" stroke="#C8963E" stroke-opacity="0.3" stroke-width="3"/>
  <text x="360" y="500" font-size="20" font-weight="bold" fill="#C8963E" text-anchor="middle">
    <tspan>{{NODE1_YEAR}}</tspan>
  </text>
  <text x="360" y="590" font-size="14" fill="#FFFFFF" text-anchor="middle">
    <tspan>{{NODE1_DESC}}</tspan>
  </text>

  <!-- Node 2 -->
  <circle cx="780" cy="540" r="10" fill="#C8963E"/>
  <circle cx="780" cy="540" r="18" fill="none" stroke="#C8963E" stroke-opacity="0.3" stroke-width="3"/>
  <text x="780" y="500" font-size="20" font-weight="bold" fill="#C8963E" text-anchor="middle">
    <tspan>{{NODE2_YEAR}}</tspan>
  </text>
  <text x="780" y="590" font-size="14" fill="#FFFFFF" text-anchor="middle">
    <tspan>{{NODE2_DESC}}</tspan>
  </text>

  <!-- Node 3 -->
  <circle cx="1200" cy="540" r="10" fill="#C8963E"/>
  <circle cx="1200" cy="540" r="18" fill="none" stroke="#C8963E" stroke-opacity="0.3" stroke-width="3"/>
  <text x="1200" y="500" font-size="20" font-weight="bold" fill="#C8963E" text-anchor="middle">
    <tspan>{{NODE3_YEAR}}</tspan>
  </text>
  <text x="1200" y="590" font-size="14" fill="#FFFFFF" text-anchor="middle">
    <tspan>{{NODE3_DESC}}</tspan>
  </text>

  <!-- Page number -->
  <text x="1800" y="1060" font-size="14" fill="#666666" text-anchor="end">
    <tspan>{{PAGE_NUM}}</tspan>
  </text>
</svg>
```

### 5. image-text — Image + text split page

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" font-family="Microsoft YaHei, sans-serif">
  <rect width="1920" height="1080" fill="#0A1628"/>

  <!-- Header bar -->
  <rect x="120" y="80" width="1680" height="3" fill="#C8963E"/>
  <text x="120" y="160" font-size="22" font-weight="bold" fill="#FFFFFF">
    <tspan>{{PAGE_TITLE}}</tspan>
  </text>

  <!-- Left: Image area -->
  <rect x="120" y="200" width="840" height="780" rx="8" fill="#1A2A45"/>
  <image x="120" y="200" width="840" height="780" preserveAspectRatio="xMidYMid slice" href="{{IMAGE_PATH}}"/>
  <rect x="120" y="200" width="840" height="780" rx="8" fill="none" stroke="#C8963E" stroke-width="2"/>

  <!-- Right: Text area -->
  <rect x="1020" y="200" width="780" height="780" rx="8" fill="#F5F3EE"/>
  <text x="1060" y="280" font-size="22" font-weight="bold" fill="#1F3A5F">
    <tspan>{{TEXT_TITLE}}</tspan>
  </text>
  <rect x="1060" y="300" width="60" height="3" fill="#C8963E"/>
  <text x="1060" y="350" font-size="15" fill="#2D2D2D">
    <tspan>{{TEXT_LINE_1}}</tspan>
  </text>
  <text x="1060" y="385" font-size="15" fill="#2D2D2D">
    <tspan>{{TEXT_LINE_2}}</tspan>
  </text>

  <!-- Page number -->
  <text x="1800" y="1060" font-size="14" fill="#666666" text-anchor="end">
    <tspan>{{PAGE_NUM}}</tspan>
  </text>
</svg>
```

### 6. header-only — Title-only transition page

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" font-family="Microsoft YaHei, sans-serif">
  <rect width="1920" height="1080" fill="#0A1628"/>

  <!-- Section label -->
  <text x="960" y="420" font-size="18" fill="#C8963E" text-anchor="middle" letter-spacing="6">
    <tspan>{{SECTION_NUM}}</tspan>
  </text>

  <!-- Main title -->
  <text x="960" y="520" font-size="42" font-weight="bold" fill="#FFFFFF" text-anchor="middle">
    <tspan>{{SECTION_TITLE}}</tspan>
  </text>

  <!-- Gold accent line -->
  <rect x="860" y="550" width="200" height="3" fill="#C8963E"/>

  <!-- Subtitle -->
  <text x="960" y="610" font-size="18" fill="#AAAAAA" text-anchor="middle">
    <tspan>{{SUBTITLE}}</tspan>
  </text>
</svg>
```

## Safety Rules (MUST follow — violation causes text loss in PPTX export)

### Rule 1: All-tspan, no mixed direct text

❌ NEVER: `<text>Hello<tspan>World</tspan></text>` — the "World" tspan and trailing text will be lost.
✅ ALWAYS: Wrap everything in tspan. Even a single line:

```svg
<text x="100" y="200" font-size="15" fill="#2D2D2D">
  <tspan>Hello World</tspan>
</text>
```

Multi-line with different styles:

```svg
<text x="100" y="200" font-size="15" fill="#2D2D2D">
  <tspan font-weight="bold">Title line</tspan>
</text>
<text x="100" y="230" font-size="13" fill="#666666">
  <tspan>Subtitle line</tspan>
</text>
```

### Rule 2: No fullwidth space (U+3000) as leading character

❌ NEVER: `<tspan>　　Indented text</tspan>` — entire text element silently dropped.
✅ ALWAYS: Use x coordinate for indentation, remove leading U+3000:

```svg
<text x="140" y="200" font-size="15" fill="#2D2D2D">
  <tspan>Indented text</tspan>
</text>
```

### Rule 3: Break at semantic boundaries

❌ NEVER break mid-word: `近千张/实拍照片`
✅ ALWAYS break at punctuation or word boundaries: `近千张实拍/照片`

### Rule 4: Check line width before finalizing

Chinese character ≈ font-size px wide. Calculate total line width:
- Line width = (Chinese chars × fs) + (digits × fs × 0.55) + (punctuation × fs × 0.5)
- Line width MUST be ≤ container width
- If it overflows, break earlier

### Rule 5: Image aspect ratio must match original

❌ NEVER: hardcode a 4:3 image into a 16:9 frame — creates ugly whitespace.
✅ ALWAYS: read original image dimensions, set frame to exact ratio, use `preserveAspectRatio="xMidYMid slice"` for zero-crop fitting.

### Rule 6: Do NOT wrap image in `<g clip-path>`

❌ NEVER: `<g clip-path="url(#clip)"><image .../></g>` — some converters reject this structure.
✅ ALWAYS: put clip-path directly on `<image>` if cropping is needed, or use `slice` + exact frame ratio to avoid clipping entirely.

## Quality Checklist (run before exporting)

Go through this list for every page before export:

- [ ] Every `<text>` element uses ONLY `<tspan>` children (no bare text nodes)
- [ ] No U+3000 (fullwidth space) as first character of any tspan
- [ ] All line breaks are at punctuation or semantic word boundaries
- [ ] No two adjacent pages use the exact same card style (layout fatigue)
- [ ] All font-sizes on this page are from a single size ladder (e.g., 22/18/15/12, not 18/15/14/17/13)
- [ ] Image frames use original image aspect ratio
- [ ] No `<g clip-path>` wrapping `<image>`
- [ ] Spacing between sibling blocks is visually consistent (check both top and bottom margins)
- [ ] Action title: the page title is a conclusion statement, not a topic label

## Typography Rules

### Size Ladder

Every page must use one size ladder. Choose one:

| Ladder | Title | Subtitle | Body | Label |
|---|---|---|---|---|
| Standard | 22px | 18px | 15px | 12px |
| Impact (big number pages) | 28px | — | 18px | 14px |
| Dense (data-heavy pages) | 20px | 16px | 14px | 11px |

### Action Titles

Page titles must be **conclusion statements**, not topic labels:

| ❌ Topic label | ✅ Action title |
|---|---|
| "Market Analysis" | "Market growth slowed from 12% to 4% in Q3" |
| "Q3 Review" | "Q3 revenue beat target by 8%, CAC down 15%" |

### Visual Weight

The most important element on the page gets the largest font-size + bold + primary color. The second most important gets medium size. Source/footnote gets smallest + gray.

## How to Use This Skill

1. **Choose a template** from the 6 options above based on your content type
2. **Copy the SVG code** into your svg_output/ directory as `NN_pagename.svg`
3. **Replace `{{...}}` placeholders** with actual content
4. **Run the quality checklist** against the page before marking it complete
5. **Adjust spacing** by modifying y coordinates in 20px increments to keep visual rhythm

## Common Patterns

### Adding a gold bullet point list

```svg
<circle cx="160" cy="350" r="4" fill="#C8963E"/>
<text x="175" y="355" font-size="15" fill="#2D2D2D">
  <tspan>{{BULLET_TEXT}}</tspan>
</text>
```

Next bullet: increment y by 30px for each item.

### Adding a source / footnote

```svg
<text x="120" y="1020" font-size="11" fill="#888888">
  <tspan>{{SOURCE_TEXT}}</tspan>
</text>
```

### Adding a page number

```svg
<text x="1800" y="1060" font-size="14" fill="#666666" text-anchor="end">
  <tspan>{{PAGE_NUM}}</tspan>
</text>
```