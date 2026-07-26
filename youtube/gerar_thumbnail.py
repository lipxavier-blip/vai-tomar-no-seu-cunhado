#!/usr/bin/env python3
"""
Gera uma thumbnail 1280x720 pro YouTube: capa do episodio (borrada e
escurecida como fundo, nitida e centralizada por cima). As capas do Vai
Tomar ja vem com titulo e marca escritos na propria arte, entao a
thumbnail nao sobrepoe texto de titulo — so um badge pequeno "EP N".

Uso:
  python3 gerar_thumbnail.py --capa "<jpg/png>" --numero "1" --saida "<png>"
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_BADGE = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

BRANCO = "#FFFFFF"
ROXO_BADGE = "#5B2E8C"

W, H = 1280, 720
COVER_SIZE = 660
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


def gerar(capa_path: str, numero: str, saida: str):
    img = renderizar_fundo(capa_path)

    capa = Image.open(capa_path).convert("RGBA").resize((COVER_SIZE, COVER_SIZE))
    cover_x = (W - COVER_SIZE) // 2
    cover_y = (H - COVER_SIZE) // 2
    img.alpha_composite(capa, (cover_x, cover_y))

    draw = ImageDraw.Draw(img)

    fonte_badge = ImageFont.truetype(str(FONT_BADGE), 44)
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

    img.convert("RGB").save(saida, quality=95)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--capa", required=True)
    parser.add_argument("--numero", required=True)
    parser.add_argument("--saida", required=True)
    args = parser.parse_args()

    gerar(args.capa, args.numero, args.saida)
    print(f"Pronto: {args.saida}")
