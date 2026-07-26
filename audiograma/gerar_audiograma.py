#!/usr/bin/env python3
"""
Gera um video de audiograma (capa + onda sonora animada) a partir do
audio de um episodio do Vai Tomar no Seu Cunhado.

Sem brandbook proprio: o fundo e a propria capa do episodio, redimensionada
pra preencher o quadro, borrada e escurecida (estilo comum de audiograma),
com a capa nitida centralizada por cima. Mesma tecnica do Tem que temperar
(ffmpeg do Homebrew nao vem com libfreetype/drawtext, entao titulo e
pre-renderizado como PNG transparente via Pillow e sobreposto no video).

Uso:
  python3 gerar_audiograma.py --audio "<mp3>" --capa "<jpg/png>" --titulo "<titulo>" --saida "<mp4>"
"""

import argparse
import json
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_TITULO = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

BRANCO = "#FFFFFF"
BRANCO_RGB = (255, 255, 255)

CANVAS_W, CANVAS_H = 2560, 1440
COVER_SIZE = 760
TOP_MARGIN = 70
BOTTOM_MARGIN = 70
GAP = 45
WAVE_WIDTH = 2200
WAVE_ALTURA_MIN = 160
WAVE_ALTURA_MAX = 400
FONT_SIZE_TITULO = 84
BLUR_RADIUS = 40
ESCURECIMENTO = 130  # 0-255, opacidade da camada preta por cima do blur


def ffprobe_duration(audio_path: str) -> float:
    out = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json", audio_path,
        ],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def renderizar_fundo(capa_path: str, caminho_saida: Path):
    """Fundo = a propria capa, cover-fit no canvas, borrada e escurecida."""
    capa = Image.open(capa_path).convert("RGB")
    escala = max(CANVAS_W / capa.width, CANVAS_H / capa.height)
    nova_w, nova_h = int(capa.width * escala), int(capa.height * escala)
    capa_redimensionada = capa.resize((nova_w, nova_h), Image.LANCZOS)

    x = (nova_w - CANVAS_W) // 2
    y = (nova_h - CANVAS_H) // 2
    fundo = capa_redimensionada.crop((x, y, x + CANVAS_W, y + CANVAS_H))
    fundo = fundo.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))

    escurecedor = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, ESCURECIMENTO))
    fundo = Image.alpha_composite(fundo.convert("RGBA"), escurecedor)

    fundo.convert("RGB").save(caminho_saida)


def renderizar_titulo_png(titulo: str, caminho_saida: Path) -> tuple[int, int]:
    linhas = textwrap.wrap(titulo, width=24, break_long_words=False)[:2]
    fonte = ImageFont.truetype(str(FONT_TITULO), FONT_SIZE_TITULO)

    tmp = Image.new("RGBA", (10, 10))
    draw_tmp = ImageDraw.Draw(tmp)
    alturas_linha = []
    larguras_linha = []
    for linha in linhas:
        bbox = draw_tmp.textbbox((0, 0), linha, font=fonte)
        larguras_linha.append(bbox[2] - bbox[0])
        alturas_linha.append(bbox[3] - bbox[1])

    espacamento = 22
    largura_img = max(larguras_linha) + 40
    altura_img = sum(alturas_linha) + espacamento * (len(linhas) - 1) + 40

    img = Image.new("RGBA", (largura_img, altura_img), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y = 20
    for linha, altura in zip(linhas, alturas_linha):
        bbox = draw.textbbox((0, 0), linha, font=fonte)
        largura = bbox[2] - bbox[0]
        x = (largura_img - largura) / 2
        draw.text((x, y), linha, font=fonte, fill=BRANCO)
        y += altura + espacamento

    img.save(caminho_saida)
    return largura_img, altura_img


def gerar(audio: str, capa: str, titulo: str, saida: str):
    duracao = ffprobe_duration(audio)

    fundo_png = Path(saida).with_suffix(".fundo.png")
    renderizar_fundo(capa, fundo_png)

    titulo_png = Path(saida).with_suffix(".titulo.png")
    _, titulo_altura = renderizar_titulo_png(titulo, titulo_png)

    cover_y = TOP_MARGIN
    titulo_y = cover_y + COVER_SIZE + GAP
    wave_y = titulo_y + titulo_altura + GAP
    wave_altura = CANVAS_H - wave_y - BOTTOM_MARGIN
    wave_altura = max(WAVE_ALTURA_MIN, min(WAVE_ALTURA_MAX, wave_altura))

    filtro = (
        f"[1:v]scale={COVER_SIZE}:{COVER_SIZE}[cover];"
        f"[0:v][cover]overlay=(W-w)/2:{cover_y}[bg1];"
        f"[bg1][3:v]overlay=(W-w)/2:{titulo_y}[bg2];"
        f"[2:a]showwaves=s={WAVE_WIDTH}x{wave_altura}:mode=cline:colors=white:rate=30,"
        f"format=yuva420p[wave];"
        f"[bg2][wave]overlay=(W-w)/2:{wave_y}[outv]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(fundo_png),
        "-i", capa,
        "-i", audio,
        "-i", str(titulo_png),
        "-filter_complex", filtro,
        "-map", "[outv]", "-map", "2:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(duracao),
        saida,
    ]

    subprocess.run(cmd, check=True)
    titulo_png.unlink(missing_ok=True)
    fundo_png.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True)
    parser.add_argument("--capa", required=True)
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--saida", required=True)
    args = parser.parse_args()

    try:
        gerar(args.audio, args.capa, args.titulo, args.saida)
    except subprocess.CalledProcessError as e:
        print(f"Erro no ffmpeg: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Pronto: {args.saida}")
