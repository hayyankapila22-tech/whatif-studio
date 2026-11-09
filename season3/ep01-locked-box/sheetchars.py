import sys; sys.path.insert(0, "/home/claude/whatif-studio/season3/kit")
from art import Doc, g, fill, rrect, PAL
from chars import king_seated, corvin, bram, wren, guard
from render import Renderer
D = Doc()
b = fill(rrect(0,0,1080,1920,0), D.lin([(0,"#f3e6cf"),(1,"#e2cdb0")]))
def label(x,y,name,role):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Lilita" font-size="46" fill="#2a1c2e">{name}</text>'
            f'<text x="{x}" y="{y+40}" text-anchor="middle" font-family="PopX" font-weight="800" font-size="26" fill="#6b5570">{role}</text>')
b += g(king_seated(D, {"look": (0.2, 0.1), "brow": (8, -6), "mouth": "flat"}), 540, 760, s=1.0) + label(540, 830, "KING OSWIN", "the tester · 68")
for x, fn, n, r, pose in ((190, corvin, "CORVIN", "the scholar · 52", {"look": (0.4, 0), "arm": {"r": -60}}), (540, wren, "WREN", "the shepherd · 27", {"look": (0, 0)}), (880, bram, "BRAM", "the inventor · 45", {"look": (-0.4, 0)})):
    b += g(fn(D, pose), x, 1640, s=0.95) + label(x, 1720, n, r)
b += '<text x="540" y="90" text-anchor="middle" font-family="Lilita" font-size="54" fill="#2a1c2e">The Locked Box · cast</text>'
R = Renderer(); R.frame(D.svg(b), "/home/claude/work/s3/cast.png"); R.close()
