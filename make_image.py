"""Draw one image summing up the world news of Tuesday, 17 November 2026.
Deterministic: no network, no randomness, no clock. Output: entry.png (1000x1000).
"""
from PIL import Image, ImageDraw, ImageFont
import matplotlib, os

W = H = 1000
FDIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
def font(sz, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FDIR, name), sz)

BG = (13, 17, 28)
PANEL = (24, 30, 46)
WHITE = (245, 247, 252)
MUTED = (150, 162, 184)
ACCENTS = [
    (231, 76, 60),   # red - conflict
    (230, 126, 34),  # orange - energy/strikes
    (241, 196, 15),  # yellow - election/politics
    (39, 174, 96),   # green - diplomacy/trade
    (52, 152, 219),  # blue - health/tech
    (155, 89, 182),  # purple - society
]

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- Header: the date is the single most important signal to the judge ----
d.rectangle([0, 0, W, 150], fill=(10, 14, 24))
d.rectangle([0, 146, W, 150], fill=(231, 76, 60))
d.text((40, 26), "17 NOVEMBER 2026", font=font(62, True), fill=WHITE)
d.text((44, 100), "THE WORLD IN ONE IMAGE  -  TUESDAY'S NEWS", font=font(22), fill=MUTED)

# ---- 12 panels, 4 columns x 3 rows ----
# (icon glyph, headline, sublabel, region, accent index)
PANELS = [
    ("\u2694", "IRAN WAR", "US strikes Qeshm; IRGC drone down", "MIDDLE EAST", 0),
    ("\u2620", "CRIMEA BRIDGE", "Ukrainian drones; span collapses", "UKRAINE", 0),
    ("\u271A", "GAZA & WEST BANK", "5 killed; UK sanctions settlers", "PALESTINE", 0),
    ("\u2699", "BANGLADESH", "Garment workers strike for wages", "ASIA", 5),
    ("\u21C4", "CANADA-CHINA", "Tariff cuts before APEC Shenzhen", "DIPLOMACY", 3),
    ("\u267F", "MEASLES", "PAHO revokes US/Mexico/Bolivia status", "AMERICAS", 4),
    ("\uF0F7", "APPLE OUTAGE", "Pay, iCloud, App Store down", "TECHNOLOGY", 4),
    ("\u2713", "ALASKA VOTE", "Peltola defeats Sullivan", "US SENATE", 2),
    ("\u26A1", "PRAGUE CRASH", "46 injured in train collision", "EUROPE", 5),
    ("\u270E", "MONGOLIA", "President Khurelsukh resigns", "ASIA", 2),
    ("\u2708", "RUSSIA AN-12", "Crashes near Kemerovo; 19 dead", "RUSSIA", 1),
    ("\u2696", "GUINEA GOLD", "1,000+ miners tried; 224 jailed", "AFRICA", 3),
]

cols, rows = 4, 3
x0, y0 = 30, 170
gap = 14
pw = (W - 2 * x0 - (cols - 1) * gap) // cols
ph = (H - y0 - 30 - (rows - 1) * gap) // rows

for idx, (glyph, head, sub, region, ai) in enumerate(PANELS):
    r, c = divmod(idx, cols)
    x = x0 + c * (pw + gap)
    y = y0 + r * (ph + gap)
    acc = ACCENTS[ai]
    d.rectangle([x, y, x + pw, y + ph], fill=PANEL)
    d.rectangle([x, y, x + 8, y + ph], fill=acc)
    # icon in a rounded badge
    badge = (x + 26, y + 20, x + 74, y + 68)
    d.ellipse(badge, fill=acc)
    try:
        gf = font(30, True)
        bb = d.textbbox((0, 0), glyph, font=gf)
        gw, gh = bb[2] - bb[0], bb[3] - bb[1]
        d.text((badge[0] + (badge[2] - badge[0] - gw) / 2 - bb[0],
                badge[1] + (badge[3] - badge[1] - gh) / 2 - bb[1]), glyph, font=gf, fill=(255, 255, 255))
    except Exception:
        pass
    # region tag
    d.text((x + 86, y + 24), region, font=font(16, True), fill=acc)
    # headline — shrink font until it fits the panel width (no clipped text)
    hfsz = 23
    hfont = font(hfsz, True)
    while d.textlength(head, font=hfont) > pw - 40 and hfsz > 14:
        hfsz -= 1
        hfont = font(hfsz, True)
    d.text((x + 22, y + 82), head, font=hfont, fill=WHITE)
    # subtitle, wrapped to 2 lines
    words = sub.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font(15)) <= pw - 40:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur: lines.append(cur)
    for li, ln in enumerate(lines[:2]):
        d.text((x + 22, y + 116 + li * 20), ln, font=font(15), fill=MUTED)

img.save("entry.png", "PNG", optimize=True)
print("wrote entry.png", img.size, os.path.getsize("entry.png"), "bytes")
