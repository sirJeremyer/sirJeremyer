#!/usr/bin/env python3
"""Generate the profile README project cards.

Design language: the Apple "M-series" wallpaper — a near-black ground with soft
grey rounded-pipe light traces sweeping through it. Each card is a rounded panel
filled with a black-to-charcoal gradient that drifts a few percent toward the
project's own hue, overlaid with concentric corner arcs lit by a transparent
white gradient. No logos: the wordmark *is* the logo. Decorative motifs on the
right are drawn in greys only.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,SF Pro Display,Segoe UI,Helvetica,Arial,sans-serif"

W, H = 880, 196
R = 26                      # panel corner radius
PAD = 52                    # left text margin
MOTIF_X = 600               # decorative motifs live right of this

INK = "#F4F5F7"             # wordmark
INK_DIM = "#8B9099"         # eyebrow / subtitle
INK_BODY = "#B9BEC7"        # tagline
INK_CHIP = "#C7CCD4"        # chip label


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def panel(uid, top, bot, hue):
    """Near-black glass panel with wallpaper-style light traces.

    `hue` only ever appears as a low-opacity wash, so the card stays ~95% grey.
    """
    d = f'''  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{top}"/>
      <stop offset="1" stop-color="{bot}"/>
    </linearGradient>
    <radialGradient id="wash{uid}" cx="0.82" cy="0.04" r="0.92">
      <stop offset="0" stop-color="{hue}" stop-opacity="0.125"/>
      <stop offset="1" stop-color="{hue}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="sweep{uid}" x1="0.05" y1="0" x2="0.95" y2="0.7">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.30" stop-color="#FFFFFF" stop-opacity="0.115"/>
      <stop offset="0.62" stop-color="#FFFFFF" stop-opacity="0.045"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="edge{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.055"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.11"/>
    </linearGradient>
    <clipPath id="clip{uid}">
      <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{R}"/>
    </clipPath>
  </defs>
'''
    b = f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{R}" fill="url(#bg{uid})"/>\n'

    # Concentric rounded-corner arcs, anchored off-canvas so only the corners
    # sweep across the panel — the wallpaper's nested-pipe motif.
    b += f'  <g clip-path="url(#clip{uid})" fill="none" stroke="url(#sweep{uid})">\n'
    for i in range(5):
        x = -360
        y = 62 - i * 46
        w = 420 + i * 158
        h = 340 + i * 92
        b += (f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" '
              f'rx="{104 + i * 30}" stroke-width="{26 - i * 2}"/>\n')
    b += '  </g>\n'

    b += (f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{R}" '
          f'fill="url(#wash{uid})"/>\n')
    b += (f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{R}" fill="none" '
          f'stroke="url(#edge{uid})" stroke-width="1.5"/>\n')
    b += (f'  <path d="M{R+14} 1.75 H {W-R-14}" stroke="#FFFFFF" stroke-opacity="0.14" '
          f'stroke-width="1.5" stroke-linecap="round"/>\n')
    return d, b


def chip(x, y, label):
    """Hairline grey pill, mono label — an Apple spec-sheet tag."""
    w = max(74, 16 + 7.2 * len(label))
    s = (f'  <rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="#FFFFFF" '
         f'fill-opacity="0.045" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1.1"/>\n')
    s += (f'  <text x="{x + w/2:.0f}" y="{y + 17}" text-anchor="middle" font-family="{MONO}" '
          f'font-size="11" letter-spacing="0.5" fill="{INK_CHIP}">{esc(label)}</text>\n')
    return s, x + w + 11


def grey(x, y, w, h, r=9, fill=0.055, stroke=0.16, bar=None):
    """A desaturated motif tile: translucent white fill, hairline white border."""
    s = (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#FFFFFF" '
         f'fill-opacity="{fill}" stroke="#FFFFFF" stroke-opacity="{stroke}" '
         f'stroke-width="1.2"/>\n')
    if bar:
        s += (f'  <rect x="{x+10}" y="{y+10}" width="{min(bar, w-20)}" height="4" rx="2" '
              f'fill="#FFFFFF" fill-opacity="0.30"/>\n')
    return s


def card(name, title, subtitle, tagline, hue, top, bot, chips, motif=""):
    uid = name.replace("-", "")
    d, b = panel(uid, top, bot, hue)
    body = d + b + motif

    body += (f'  <text x="{PAD}" y="76" font-family="{SANS}" font-size="38" font-weight="600" '
             f'letter-spacing="-0.6" fill="{INK}">{esc(title)}</text>\n')
    if subtitle:
        body += (f'  <text x="{PAD+2}" y="100" font-family="{MONO}" font-size="11" '
                 f'font-weight="500" letter-spacing="3.4" fill="{INK_DIM}">{esc(subtitle)}</text>\n')
    rule_end = MOTIF_X - 32 if motif else W - PAD
    body += (f'  <path d="M{PAD} 118 H {rule_end}" stroke="#FFFFFF" stroke-opacity="0.13" '
             f'stroke-width="1.1" stroke-linecap="round"/>\n')
    body += (f'  <text x="{PAD}" y="143" font-family="{SANS}" font-size="14.5" '
             f'fill="{INK_BODY}">{esc(tagline)}</text>\n')

    x = PAD
    for label in chips:
        s, x = chip(x, 156, label)
        body += s

    alt = f"{title} — {tagline}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
           f'height="{H}" role="img" aria-label="{esc(alt)}">\n'
           f'  <title>{esc(alt)}</title>\n{body}</svg>\n')
    path = os.path.join(OUT, f"card-{name}.svg")
    with open(path, "w") as f:
        f.write(svg)
    print(f"card-{name}.svg  {len(svg):>6} bytes")


LINKEDIN_PATH = (
    "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 "
    "2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 "
    "4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 "
    "2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 "
    "23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.225 0z"
)

GITHUB_PATH = (
    "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 "
    "0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 "
    "17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 "
    "1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-"
    "2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 "
    "3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 "
    "3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 "
    "1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-"
    "6.627-5.373-12-12-12"
)


def badge(name, label, icon_path):
    """A social badge in the card language — hairline pill, mono caps, white mark.

    Generated locally rather than pulled from shields.io: its Verdana caps clash
    with the cards' mono chips, and shields.io no longer ships a LinkedIn icon
    (simple-icons dropped it), which left that badge as bare text.
    """
    bh, ic, pad, gap = 36, 17, 17, 10
    tw = 7.05 * len(label) + 1.6 * (len(label) - 1)
    bw = pad + ic + gap + tw + pad
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {bw:.0f} {bh}" '
         f'width="{bw:.0f}" height="{bh}" role="img" aria-label="{esc(label)}">\n'
         f'  <title>{esc(label)}</title>\n'
         f'  <rect x="0.7" y="0.7" width="{bw-1.4:.0f}" height="{bh-1.4}" rx="{(bh-1.4)/2:.1f}" '
         f'fill="#FFFFFF" fill-opacity="0.05" stroke="#FFFFFF" stroke-opacity="0.18" '
         f'stroke-width="1.2"/>\n'
         f'  <g transform="translate({pad},{(bh-ic)/2:.1f}) scale({ic/24:.4f})">'
         f'<path fill="#E4E7EC" d="{icon_path}"/></g>\n'
         f'  <text x="{pad + ic + gap:.0f}" y="{bh/2 + 4:.0f}" font-family="{MONO}" '
         f'font-size="12" font-weight="600" letter-spacing="1.6" fill="{INK}">'
         f'{esc(label)}</text>\n</svg>\n')
    path = os.path.join(OUT, f"badge-{name}.svg")
    with open(path, "w") as f:
        f.write(s)
    print(f"badge-{name}.svg  {len(s):>6} bytes")


# ---------------------------------------------------------------- the cards
if __name__ == "__main__":
    badge("linkedin", "LINKEDIN", LINKEDIN_PATH)
    badge("github", "GITHUB", GITHUB_PATH)


    # ECY — the widget canvas, as four grey tiles on the snap grid.
    ecy_motif = (grey(624, 40, 100, 60, bar=28)
                 + grey(736, 40, 104, 80, bar=32)
                 + grey(624, 112, 100, 44, bar=26)
                 + grey(736, 132, 104, 24, r=8, bar=30))
    card("ecy", "ECY", "EASY EFFICIENCY",
         "Thirteen desktop widgets on one canvas you summon and dismiss.",
         "#8B7BF6", "#15161A", "#0A0A0C",
         ["Swift", "SwiftUI", "Python", "Local-first"],
         motif=ecy_motif)

    # Die Klangnüsse — the endless tree: a trunk, three branches, three nuts.
    # Branches must start *at* the trunk (x=634) or the motif reads as loose bars.
    tree = grey(608, 26, 26, 148, r=6, fill=0.055, stroke=0.15)
    for i, (by, bw) in enumerate([(46, 152), (94, 186), (140, 124)]):
        o = 0.17 - i * 0.03
        tree += (f'  <rect x="634" y="{by}" width="{bw}" height="7" rx="3.5" '
                 f'fill="#FFFFFF" fill-opacity="{o:.2f}"/>\n')
        # A nut sitting *on* the branch tip reads as a slider thumb — hang it
        # underneath on a short stem instead, and add an upward twig for canopy.
        tip = 634 + bw - 4
        tree += (f'  <rect x="{tip - 1}" y="{by + 6}" width="2.4" height="8" '
                 f'fill="#FFFFFF" fill-opacity="{o + 0.06:.2f}"/>\n')
        tree += (f'  <ellipse cx="{tip}" cy="{by + 22}" rx="7.5" ry="8.5" '
                 f'fill="#FFFFFF" fill-opacity="{0.36 - i * 0.08:.2f}"/>\n')
        tree += (f'  <rect x="{634 + int(bw * 0.52)}" y="{by - 13}" width="2.4" height="14" '
                 f'fill="#FFFFFF" fill-opacity="{o:.2f}"/>\n')
    card("klangnuesse", "Die Klangnüsse", "SYMPHONY OF THE FOREST",
         "A squirrel climbs a tree — and your voice is the controller.",
         "#FFB845", "#15161A", "#0A0A0C",
         ["JavaScript", "Vite", "Web Audio", "Playwright"],
         motif=tree)

    # Jeff's Job — the desk: day counter, CRT with its quota, keyboard, payslip.
    desk = grey(612, 44, 50, 58, r=7, fill=0.05, stroke=0.16)
    desk += ('  <rect x="612" y="44" width="50" height="15" rx="7" fill="#FFFFFF" '
             'fill-opacity="0.20"/>\n')
    desk += ('  <rect x="612" y="52" width="50" height="7" fill="#FFFFFF" '
             'fill-opacity="0.20"/>\n')
    desk += (f'  <text x="637" y="90" text-anchor="middle" font-family="{MONO}" font-size="21" '
             f'font-weight="700" fill="#FFFFFF" fill-opacity="0.42">1</text>\n')
    desk += grey(672, 44, 108, 76, r=8, fill=0.05, stroke=0.18)
    desk += ('  <rect x="682" y="54" width="88" height="50" rx="3" fill="#FFFFFF" '
             'fill-opacity="0.06"/>\n')
    for i, wpx in enumerate((58, 44, 66, 36)):
        desk += (f'  <rect x="690" y="{62 + i*10}" width="{wpx}" height="4" rx="2" '
                 f'fill="#FFFFFF" fill-opacity="0.26"/>\n')
    desk += grey(672, 132, 108, 16, r=5, fill=0.05, stroke=0.14)
    desk += (f'  <text x="844" y="62" text-anchor="end" font-family="{MONO}" font-size="18" '
             f'font-weight="700" letter-spacing="1" fill="#FFFFFF" '
             f'fill-opacity="0.50">500$</text>\n')
    card("gamejam", "Jeff's Job", "GAME JAM ULM 2025",
         "Stamp the quota, answer the phone, keep the family — pick two.",
         "#A79BD1", "#15161A", "#0A0A0C",
         ["Godot 4.5", "GDScript", "Narrative 2D", "Team project"],
         motif=desk)
