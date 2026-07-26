#!/usr/bin/env python3
"""
Gera um video de audiograma (capa + onda sonora animada) a partir do
audio de um episodio do Vai Tomar no Seu Cunhado.

Sem brandbook proprio: o fundo e a propria capa do episodio, redimensionada
pra preencher o quadro, borrada e escurecida (estilo comum de audiograma),
com a capa nitida centralizada por cima. As capas do Vai Tomar ja vem com
titulo e marca escritos na propria arte, entao o video nao sobrepoe texto
nenhum — so capa + onda sonora.

Uso:
  python3 gerar_audiograma.py --audio "<mp3>" --capa "<jpg/png>" --saida "<mp4>"
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageFilter

CANVAS_W, CANVAS_H = 2560, 1440
COVER_SIZE = 1000
TOP_MARGIN = 90
BOTTOM_MARGIN = 90
GAP = 60
WAVE_WIDTH = 2200
WAVE_ALTURA_MIN = 160
WAVE_ALTURA_MAX = 400
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


def gerar(audio: str, capa: str, saida: str):
    duracao = ffprobe_duration(audio)

    fundo_png = Path(saida).with_suffix(".fundo.png")
    renderizar_fundo(capa, fundo_png)

    cover_y = TOP_MARGIN
    wave_y = cover_y + COVER_SIZE + GAP
    wave_altura = CANVAS_H - wave_y - BOTTOM_MARGIN
    wave_altura = max(WAVE_ALTURA_MIN, min(WAVE_ALTURA_MAX, wave_altura))

    filtro = (
        f"[1:v]scale={COVER_SIZE}:{COVER_SIZE}[cover];"
        f"[0:v][cover]overlay=(W-w)/2:{cover_y}[bg1];"
        f"[2:a]showwaves=s={WAVE_WIDTH}x{wave_altura}:mode=cline:colors=white:rate=30,"
        f"format=yuva420p[wave];"
        f"[bg1][wave]overlay=(W-w)/2:{wave_y}[outv]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(fundo_png),
        "-i", capa,
        "-i", audio,
        "-filter_complex", filtro,
        "-map", "[outv]", "-map", "2:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(duracao),
        saida,
    ]

    subprocess.run(cmd, check=True)
    fundo_png.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True)
    parser.add_argument("--capa", required=True)
    parser.add_argument("--saida", required=True)
    args = parser.parse_args()

    try:
        gerar(args.audio, args.capa, args.saida)
    except subprocess.CalledProcessError as e:
        print(f"Erro no ffmpeg: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Pronto: {args.saida}")
