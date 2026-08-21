#!/usr/bin/env python3
"""Generate the profile README project cards.

Same visual language as the ECY repo's README cards: a rounded translucent
"glass" panel with a dotted canvas texture, a hairline accent border and a
highlight along the top edge. Each card carries a pixel-art logo, the project
name, a one-line tagline and a row of stack chips.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"

W, H = 880, 184


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def panel(uid, top, bot, accent, r=22):
    """Rounded translucent-glass panel: gradient fill, canvas dots, hairline border."""
    d = f'''  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0" stop-color="{top}"/>
      <stop offset="1" stop-color="{bot}"/>
    </linearGradient>
    <pattern id="dot{uid}" width="34" height="34" patternUnits="userSpaceOnUse">
      <rect x="13" y="13" width="9" height="9" rx="2.6" fill="#FFFFFF" opacity="0.045"/>
    </pattern>
  </defs>
'''
    b = f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{r}" fill="url(#bg{uid})"/>\n'
    b += f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{r}" fill="url(#dot{uid})"/>\n'
    b += (f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{r}" fill="none" '
          f'stroke="{accent}" stroke-opacity="0.30" stroke-width="1.5"/>\n')
    b += (f'  <path d="M{r+8} 1.75 H {W-r-8}" stroke="#FFFFFF" stroke-opacity="0.10" '
          f'stroke-width="1.5" stroke-linecap="round"/>\n')
    return d, b


def chip(x, y, label, color, w=None):
    """Pill-shaped stack chip, mono label, tinted to the given colour."""
    w = w or max(78, 15 + 7.4 * len(label))
    s = (f'  <rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="{color}" '
         f'fill-opacity="0.14" stroke="{color}" stroke-opacity="0.40" stroke-width="1.2"/>\n')
    s += (f'  <text x="{x + w/2:.0f}" y="{y + 17}" text-anchor="middle" font-family="{MONO}" '
          f'font-size="11" letter-spacing="0.6" fill="{color}">{esc(label)}</text>\n')
    return s, x + w + 12


def logo(pixels, x, y, size):
    """Place a pixel-art logo (list of <rect> strings on a 128-unit grid)."""
    scale = size / 128.0
    return (f'  <g transform="translate({x},{y}) scale({scale:.4f})" '
            f'shape-rendering="crispEdges">{"".join(pixels)}</g>\n')


def tile(x, y, w, h, color):
    """A translucent widget tile, echoing the ECY hero's canvas motif."""
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{color}" '
            f'fill-opacity="0.16" stroke="{color}" stroke-opacity="0.42" stroke-width="1.4"/>\n'
            f'  <rect x="{x+9}" y="{y+9}" width="{min(28, w-18)}" height="4" rx="2" '
            f'fill="{color}" fill-opacity="0.75"/>\n')


def card(name, title, subtitle, tagline, accent, top, bot, pixels, chips, motif="",
         title_fill=None, defs_extra=""):
    uid = name.replace("-", "")
    d, b = panel(uid, top, bot, accent)
    if defs_extra:
        d = d.replace("  </defs>", defs_extra + "  </defs>")
    body = d + b + motif
    body += logo(pixels, 34, 34, 116)
    tx = 186
    body += (f'  <text x="{tx}" y="66" font-family="{MONO}" font-size="27" font-weight="700" '
             f'letter-spacing="2.2" fill="{title_fill or accent}">{esc(title)}</text>\n')
    if subtitle:
        body += (f'  <text x="{tx+2}" y="90" font-family="{MONO}" font-size="12" '
                 f'font-weight="600" letter-spacing="2.8" fill="{accent}" '
                 f'fill-opacity="0.75">{esc(subtitle)}</text>\n')
    rule_end = 590 if motif else W - 40
    body += (f'  <path d="M{tx} 106 H {rule_end}" stroke="{accent}" stroke-opacity="0.18" '
             f'stroke-width="1.2" stroke-linecap="round"/>\n')
    body += (f'  <text x="{tx}" y="130" font-family="{SANS}" font-size="14.5" fill="#E6EAF2" '
             f'fill-opacity="0.86">{esc(tagline)}</text>\n')
    x = tx
    for label, color in chips:
        s, x = chip(x, 143, label, color)
        body += s
    label = f"{title} — {tagline}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
           f'height="{H}" role="img" aria-label="{esc(label)}">\n'
           f'  <title>{esc(label)}</title>\n{body}</svg>\n')
    path = os.path.join(OUT, f"card-{name}.svg")
    with open(path, "w") as f:
        f.write(svg)
    print(f"card-{name}.svg  {len(svg):>6} bytes")


# ---------------------------------------------------------------- the cards
if __name__ == "__main__":
    from pixels_ecy import ECY
    from pixels_gamejam import GAMEJAM
    from pixels_klangnuesse import KLANGNUESSE

    # ECY — echoes its own README: violet border, gradient wordmark, canvas tiles.
    ecy_motif = (tile(652, 30, 96, 54, "#4DA6FF") + tile(760, 30, 98, 74, "#F5A623")
                 + tile(652, 96, 96, 58, "#4ADE80") + tile(760, 116, 98, 38, "#F87171"))
    ecy_grad = '''    <linearGradient id="wmecy" x1="0" y1="0" x2="1" y2="0.6">
      <stop offset="0" stop-color="#FBBF24"/>
      <stop offset="0.5" stop-color="#F87171"/>
      <stop offset="1" stop-color="#8B7BF6"/>
    </linearGradient>
'''
    card("ecy", "ECY", "EASY EFFICIENCY",
         "Thirteen desktop widgets on one canvas you summon and dismiss.",
         "#8B7BF6", "#2C3040", "#1C1F2B", ECY,
         [("Swift", "#4DA6FF"), ("SwiftUI", "#FBBF24"), ("Python", "#4ADE80"),
          ("Local-first", "#A78BFA")],
         motif=ecy_motif, title_fill="url(#wmecy)", defs_extra=ecy_grad)

    # Die Klangnuesse — the game's own palette: violet night, gold, pixel branches.
    branches = ""
    for i, (bx, by, bw) in enumerate([(690, 46, 150), (648, 88, 150), (706, 130, 134)]):
        branches += (f'  <rect x="{bx}" y="{by}" width="{bw}" height="9" rx="2" '
                     f'fill="#B06222" fill-opacity="0.55"/>\n')
        branches += (f'  <rect x="{bx + bw - 26}" y="{by - 15}" width="14" height="14" rx="3" '
                     f'fill="#FFB845" fill-opacity="{0.8 - i * 0.16:.2f}"/>\n')
    trunk = ('  <rect x="612" y="26" width="30" height="132" rx="4" fill="#B06222" '
             'fill-opacity="0.30"/>\n')
    card("klangnuesse", "DIE KLANGNÜSSE", "SYMPHONY OF THE FOREST",
         "A squirrel climbs a tree — and your voice is the controller.",
         "#FFB845", "#2A1D44", "#1A1228", KLANGNUESSE,
         [("JavaScript", "#FBBF24"), ("Vite", "#A78BFA"), ("Web Audio", "#4ADE80"),
          ("Playwright", "#4DA6FF")],
         motif=trunk + branches)

    # Game Jam Ulm 2025 — the game's own hand-drawn desk: olive wall, CRT, green payslip.
    desk = ""
    desk += ('  <rect x="616" y="36" width="52" height="58" rx="4" fill="#E6DFF0" '
             'fill-opacity="0.20" stroke="#E6DFF0" stroke-opacity="0.38" stroke-width="1.4"/>\n')
    desk += ('  <rect x="616" y="36" width="52" height="15" rx="4" fill="#C0392B" '
             'fill-opacity="0.45"/>\n')
    desk += (f'  <text x="642" y="80" text-anchor="middle" font-family="{MONO}" font-size="21" '
             'font-weight="700" fill="#E6DFF0" fill-opacity="0.55">1</text>\n')
    desk += ('  <rect x="676" y="36" width="108" height="76" rx="7" fill="#9A93B8" '
             'fill-opacity="0.20" stroke="#9A93B8" stroke-opacity="0.45" stroke-width="1.4"/>\n')
    desk += ('  <rect x="686" y="46" width="88" height="50" rx="3" fill="#E6DFF0" '
             'fill-opacity="0.22"/>\n')
    for i, wpx in enumerate((60, 46, 68, 38)):
        desk += (f'  <rect x="694" y="{54 + i*10}" width="{wpx}" height="4" rx="2" '
                 'fill="#E6DFF0" fill-opacity="0.45"/>\n')
    desk += ('  <rect x="676" y="124" width="108" height="16" rx="4" fill="#B9B9C4" '
             'fill-opacity="0.24" stroke="#B9B9C4" stroke-opacity="0.36" stroke-width="1.2"/>\n')
    desk += (f'  <text x="852" y="52" text-anchor="end" font-family="{MONO}" font-size="19" '
             'font-weight="700" letter-spacing="1" fill="#3BE55A" fill-opacity="0.85">500$</text>\n')
    card("gamejam", "JEFF'S JOB", "GAME JAM ULM 2025",
         "Stamp the quota, answer the phone, keep the family — pick two.",
         "#A79BD1", "#3A3826", "#221F16", GAMEJAM,
         [("Godot 4.5", "#478CBF"), ("GDScript", "#A79BD1"), ("Narrative 2D", "#4ADE80"),
          ("Team project", "#E8A33D")],
         motif=desk)
