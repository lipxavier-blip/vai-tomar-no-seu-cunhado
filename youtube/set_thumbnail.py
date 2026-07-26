#!/usr/bin/env python3
"""
Define a thumbnail customizada de um video ja existente no YouTube.
Usa o mesmo escopo de upload (youtube.upload) ja autorizado.

Uso:
  python3 set_thumbnail.py --video-id <id> --imagem "<png/jpg>"
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import requests

ENV_PATH = Path(__file__).parent.parent / ".env.local"


def carregar_env():
    env = {}
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k, v = line.split("=", 1)
            env[k] = v
    return env


def salvar_access_token(novo_token: str):
    linhas = ENV_PATH.read_text().splitlines()
    for i, linha in enumerate(linhas):
        if linha.startswith("YOUTUBE_ACCESS_TOKEN="):
            linhas[i] = f"YOUTUBE_ACCESS_TOKEN={novo_token}"
    ENV_PATH.write_text("\n".join(linhas) + "\n")


def renovar_token(env: dict) -> str:
    data = urllib.parse.urlencode({
        "client_id": env["YOUTUBE_CLIENT_ID"],
        "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        token_data = json.loads(resp.read())
    salvar_access_token(token_data["access_token"])
    return token_data["access_token"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--imagem", required=True)
    args = parser.parse_args()

    env = carregar_env()
    token = renovar_token(env)

    with open(args.imagem, "rb") as f:
        resp = requests.post(
            "https://www.googleapis.com/upload/youtube/v3/thumbnails/set",
            params={"videoId": args.video_id},
            headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"},
            data=f,
        )

    if not resp.ok:
        print(f"Erro: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)

    print("Thumbnail definida.")
