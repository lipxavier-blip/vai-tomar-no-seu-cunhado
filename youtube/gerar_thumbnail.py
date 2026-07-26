#!/usr/bin/env python3
"""
Gera uma thumbnail 1280x720 pro YouTube: capa do episodio (borrada e
escurecida como fundo, nitida e centralizada por cima) + titulo em letra
grande (legivel em miniatura) + badge "EP N". Mesmo estilo visual do
audiograma (gerar_audiograma.py) — sem brandbook proprio, so a capa do
episodio.

Uso:
  python3 gerar_thumbnail.py --capa "<jpg/png>" --titulo "<titulo>" --numero "1" --saida "<png>"
"""

import argparse
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_TITULO = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

BRANCO = "#FFFFFF"
ROXO_BADGE = "#5B2E8C"

W, H = 1280, 720
COVER_SIZE = 520
BLUR_RADIUS = 30
ESCURECIMENTO = 140


def renderizar_fundo(capa_path: str) -> Image.Image:
    capa = Image.open(capa_path).convert("RGB")
    escala = max(W / capa.width, H / capa.height)
    nova_w, nova_h = int(capa.width * escala), int(capa.height * escala)
    capa_redimensionada = capa.resize((nova_w, nova_h), Image.LANCZOS)

    x = (nova_w - W) // 2
    y = (nova_h - H) // 2
    fundo = capa_redimensionada.crop((x, y, x + W, y + H))
    fundo = fundo.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))

    escurecedor = Image.new("RGBA", (W, H), (0, 0, 0, ESCURECIMENTO))
    return Image.alpha_composite(fundo.convert("RGBA"), escurecedor)


def gerar(capa_path: str, titulo: str, numero: str, saida: str):
    img = renderizar_fundo(capa_path)

    capa = Image.open(capa_path).convert("RGBA").resize((COVER_SIZE, COVER_SIZE))
    cover_x = W - COVER_SIZE - 40
    cover_y = (H - COVER_SIZE) // 2
    img.alpha_composite(capa, (cover_x, cover_y))

    draw = ImageDraw.Draw(img)

    fonte_badge = ImageFont.truetype(str(FONT_TITULO), 44)
    badge_texto = f"EP {numero}"
    bbox = draw.textbbox((0, 0), badge_texto, font=fonte_badge)
    badge_w = bbox[2] - bbox[0] + 56
    badge_h = bbox[3] - bbox[1] + 34
    badge_x, badge_y = 60, 70
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=badge_h // 2, fill=ROXO_BADGE,
    )
    draw.text(
        (badge_x + 28, badge_y + 14), badge_texto, font=fonte_badge, fill=BRANCO,
    )

    largura_max_titulo = 26
    fonte_titulo = ImageFont.truetype(str(FONT_TITULO), 96)
    linhas = textwrap.wrap(titulo, width=largura_max_titulo, break_long_words=False)[:3]

    while True:
        alturas = [draw.textbbox((0, 0), l, font=fonte_titulo)[3] for l in linhas]
        largura_maxima = max(draw.textbbox((0, 0), l, font=fonte_titulo)[2] for l in linhas)
        bloco_altura = sum(alturas) + 20 * (len(linhas) - 1)
        if largura_maxima <= W - COVER_SIZE - 140 and bloco_altura <= H - 260:
            break
        fonte_titulo = ImageFont.truetype(str(FONT_TITULO), fonte_titulo.size - 6)
        if fonte_titulo.size < 48:
            break

    y = (H - bloco_altura) // 2 + 30
    for linha in linhas:
        draw.text((60, y), linha, font=fonte_titulo, fill=BRANCO)
        bbox = draw.textbbox((0, 0), linha, font=fonte_titulo)
        y += (bbox[3] - bbox[1]) + 20

    img.convert("RGB").save(saida, quality=95)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--capa", required=True)
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--numero", required=True)
    parser.add_argument("--saida", required=True)
    args = parser.parse_args()

    gerar(args.capa, args.titulo, args.numero, args.saida)
    print(f"Pronto: {args.saida}")
