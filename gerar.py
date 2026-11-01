#!/usr/bin/env python3
"""Gera as imagens do perfil (PNG) a partir de SVGs desenhados em código.
Edite a seção CONFIG e rode:  python3 gerar.py
Precisa do rsvg-convert (librsvg) instalado. Fonte usada: Poppins."""
import subprocess, pathlib, os, json

# ================= CONFIG =================
NOME_BANNER = "Oi, eu sou a Dani"
SUBTITULO   = "bem-vinda ao meu cantinho de código"
TECNOLOGIAS = ["HTML", "CSS", "JavaScript", "Git", "[sua tech]"]
NUMEROS     = [("0", "repositórios"), ("0", "estrelas"), ("0", "commits no ano")]
# ==========================================
# a Action do GitHub passa os números reais por esta variável
if os.environ.get("NUMEROS"):
    NUMEROS = [tuple(x) for x in json.loads(os.environ["NUMEROS"])]
# semanas de contribuições (lista de semanas, cada uma com até 7 contagens)
SEMANAS = json.loads(os.environ["CONTRIB"]) if os.environ.get("CONTRIB") else [[0]*7 for _ in range(53)]

OUT = pathlib.Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

PLUM_BG = "#2a1520"; CARD = "#2b1621"; BORDER = "#4d2a3d"
PINK = "#ff8fb8"; PINK_L = "#ffc2d9"; DARK = "#2a1520"; FONT = "Poppins, sans-serif"

def cat(x, y, s, eyes="open", face="#ffffff", ear_in="#ffb3cf"):
    eye = (f'<circle cx="-22" cy="4" r="4.6" fill="{DARK}"/><circle cx="22" cy="4" r="4.6" fill="{DARK}"/>'
           '<circle cx="-20.6" cy="2.4" r="1.5" fill="#fff"/><circle cx="23.4" cy="2.4" r="1.5" fill="#fff"/>'
           if eyes == "open" else
           f'<path d="M-29 6 Q-22 -3 -15 6 M15 6 Q22 -3 29 6" stroke="{DARK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>')
    return f'''<g transform="translate({x},{y}) scale({s})">
  <polygon points="-47,-4 -43,-52 -10,-30" fill="{face}" stroke="{PINK}" stroke-width="4" stroke-linejoin="round"/>
  <polygon points="47,-4 43,-52 10,-30" fill="{face}" stroke="{PINK}" stroke-width="4" stroke-linejoin="round"/>
  <polygon points="-40,-14 -38,-40 -20,-28" fill="{ear_in}"/>
  <polygon points="40,-14 38,-40 20,-28" fill="{ear_in}"/>
  <ellipse cx="0" cy="6" rx="52" ry="42" fill="{face}" stroke="{PINK}" stroke-width="4"/>
  <ellipse cx="-33" cy="17" rx="10" ry="6.5" fill="#ff9fc3" opacity=".75"/>
  <ellipse cx="33" cy="17" rx="10" ry="6.5" fill="#ff9fc3" opacity=".75"/>
  {eye}
  <path d="M-4 13 L4 13 L0 18 Z" fill="#ff6fa3" stroke="#ff6fa3" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M0 18 Q-5 25 -11 20 M0 18 Q5 25 11 20" stroke="{DARK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
  <path d="M-46 9 L-64 5 M-46 16 L-63 19 M46 9 L64 5 M46 16 L63 19" stroke="{DARK}" stroke-width="2" stroke-linecap="round"/>
</g>'''

def flower(x, y, r, petal="#ffffff", center="#ffd23f", rot=0, ring="#f3dbe6"):
    ps = "".join(f'<ellipse cx="0" cy="{-r*0.56}" rx="{r*0.42}" ry="{r*0.52}" fill="{petal}" stroke="{ring}" stroke-width="{r*0.06}" transform="rotate({72*i})"/>' for i in range(5))
    return (f'<g transform="translate({x},{y}) rotate({rot})">{ps}'
            f'<circle r="{r*0.3}" fill="{center}" stroke="#f0a92b" stroke-width="{r*0.05}"/></g>')

def save(name, svg, w, h, scale=2, png=False):
    """Salva SVG puro (texto já convertido em desenho, sem depender de fonte).
    O avatar sai em PNG porque o GitHub só aceita imagem para foto de perfil."""
    src = OUT / f"_{name}.svg"; src.write_text(svg, encoding="utf-8")
    if png:
        subprocess.run(["rsvg-convert", "-w", str(w*scale), "-h", str(h*scale), str(src), "-o", str(OUT / f"{name}.png")], check=True)
    else:
        subprocess.run(["rsvg-convert", "-f", "svg", str(src), "-o", str(OUT / f"{name}.svg")], check=True)
    src.unlink()

# ---------- avatar ----------
avatar = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 500 500">
<rect width="500" height="500" fill="{PLUM_BG}"/>
<circle cx="250" cy="250" r="236" fill="#2f1824" stroke="{PINK}" stroke-width="9"/>
{cat(250, 262, 3.3)}
{flower(250+36*3.3, 262-46*3.3, 15*3.3, petal=PINK, center="#ffd23f", ring="#ffb3cf")}
</svg>'''
save("avatar", avatar, 500, 500, 1, png=True)

# ---------- banner ----------
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="330" viewBox="0 0 1020 330">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#6a2853"/><stop offset="1" stop-color="#93345f"/></linearGradient></defs>
<rect width="1020" height="330" fill="url(#g)"/>
{flower(76, 68, 29, rot=10)}
{flower(782, 60, 25, rot=-8)}
{flower(960, 250, 17, rot=20)}
{cat(172, 208, 1.15, eyes="closed")}
{cat(858, 196, 1.3, eyes="open", face="#ffc9dc", ear_in="#ff9fc3")}
<text x="510" y="166" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="54" fill="#ffffff">{NOME_BANNER}</text>
<text x="510" y="203" text-anchor="middle" font-family="{FONT}" font-weight="500" font-size="21" fill="#ffe3ee">{SUBTITULO}</text>
</svg>'''
save("banner", banner, 1020, 330)

# ---------- ferramentas (chips) ----------
chips, x = [], 2
for t in TECNOLOGIAS:
    w = int(len(t) * 11.2 + 40)
    chips.append(f'<rect x="{x}" y="4" width="{w}" height="46" rx="23" fill="#3b1b2d" stroke="#7a3d5e" stroke-width="2"/>'
                 f'<text x="{x+w/2}" y="33" text-anchor="middle" font-family="{FONT}" font-weight="600" font-size="17" fill="#ffffff">{t}</text>')
    x += w + 14
W = x
ferr = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="54" viewBox="0 0 {W} 54">{"".join(chips)}</svg>'
save("ferramentas", ferr, W, 54)

# ---------- números ----------
cw, gap = 316, 16
cards = []
for i, (n, label) in enumerate(NUMEROS):
    cx = 2 + i * (cw + gap)
    cards.append(f'<rect x="{cx}" y="2" width="{cw}" height="118" rx="18" fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>'
                 f'<text x="{cx+24}" y="60" font-family="{FONT}" font-weight="700" font-size="36" fill="{PINK}">{n}</text>'
                 f'<text x="{cx+24}" y="92" font-family="{FONT}" font-weight="400" font-size="16" fill="{PINK_L}">{label}</text>')
W2 = 2 + len(NUMEROS) * (cw + gap) - gap + 2
nums = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="122" viewBox="0 0 {W2} 122">{"".join(cards)}</svg>'
save("numeros", nums, W2, 122)


# ---------- contribuições ----------
NIVEIS = ["#3b1a2d", "#6e2a55", "#b03a72", "#ff8fb8", "#ffe0ec"]
def nivel(n, mx):
    if n <= 0 or mx <= 0: return 0
    r = n / mx
    return 1 if r <= .25 else 2 if r <= .5 else 3 if r <= .75 else 4
mx = max((d for sem in SEMANAS for d in sem), default=0)
C, G = 13, 4
nsem = len(SEMANAS)
gw = nsem * (C + G) - G
CW = gw + 56
CH = 7 * (C + G) - G + 118
quad = []
for i, sem in enumerate(SEMANAS):
    for j, d in enumerate(sem):
        quad.append(f'<rect x="{28 + i*(C+G)}" y="{64 + j*(C+G)}" width="{C}" height="{C}" rx="3" fill="{NIVEIS[nivel(d, mx)]}"/>')
leg_x = CW - 28 - (5 * (C + G) + 96)
leg = "".join(f'<rect x="{leg_x + 52 + k*(C+G)}" y="{CH-42}" width="{C}" height="{C}" rx="3" fill="{c}"/>' for k, c in enumerate(NIVEIS))
contrib = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">
<rect x="2" y="2" width="{CW-4}" height="{CH-4}" rx="18" fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>
<text x="28" y="42" font-family="{FONT}" font-weight="700" font-size="18" fill="#ffffff">Minhas contribuições</text>
{"".join(quad)}
<text x="{leg_x}" y="{CH-31}" font-family="{FONT}" font-size="12" fill="{PINK_L}">menos</text>
{leg}
<text x="{leg_x + 52 + 5*(C+G) + 4}" y="{CH-31}" font-family="{FONT}" font-size="12" fill="{PINK_L}">mais</text>
</svg>'''
save("contribuicoes", contrib, CW, CH)

# ---------- flores (rodapé) ----------
flores = f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="60" viewBox="0 0 200 60">
{flower(30, 30, 20, petal="#ff9fc3", ring="#ff7fb0", rot=5)}
{flower(100, 30, 14, petal="#ffc2d9", ring="#ff9fc3", rot=-10)}
{flower(170, 30, 20, petal="#ff9fc3", ring="#ff7fb0", rot=15)}
</svg>'''
save("flores", flores, 200, 60)
print("ok ->", OUT)
