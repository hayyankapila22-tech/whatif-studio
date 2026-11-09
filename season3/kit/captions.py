"""Channel subtitle style: Lilita One, white with a thick plum outline + soft shadow, the spoken word in gold.
Sits in the safe band (centre y ~1330, never above faces, never below y=1440)."""
from art import INK, W
from xml.sax.saxutils import escape


def subtitle(words, active=-1, y=1330, size=78, maxw=900, pop=1.0):
    """words: list of str for the current phrase (<= ~6 words); active = index being spoken."""
    # rough line wrap by character count
    lines, cur = [], []
    for i, w in enumerate(words):
        test = " ".join(x for _, x in cur + [(i, w)])
        if cur and len(test) * size * 0.5 > maxw:
            lines.append(cur)
            cur = []
        cur.append((i, w))
    if cur:
        lines.append(cur)
    lh = size * 1.08
    y0 = y - (len(lines) - 1) * lh / 2
    out = ""
    for li, ln in enumerate(lines):
        yy = y0 + li * lh
        spans_o, spans_f = "", ""
        for i, w in ln:
            on = i == active
            col = "#ffd25a" if on else "#ffffff"
            sz = size * (pop if on else 1.0)
            spans_o += f'<tspan font-size="{sz:.1f}">{escape(w)} </tspan>'
            spans_f += f'<tspan fill="{col}" font-size="{sz:.1f}">{escape(w)} </tspan>'
        base = f'x="{W/2}" y="{yy:.1f}" text-anchor="middle" font-family="Lilita" letter-spacing="1"'
        out += f'<text {base} fill="#140a1c" opacity="0.45" transform="translate(0,7)">{spans_o}</text>'
        out += f'<text {base} fill="none" stroke="{INK}" stroke-width="{size*0.2:.1f}" stroke-linejoin="round">{spans_o}</text>'
        out += f'<text {base}>{spans_f}</text>'
    return out
