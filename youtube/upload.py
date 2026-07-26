#!/usr/bin/env python3
"""
Sobe um video pro YouTube via upload resumivel da Data API v3.

Sempre renova o access_token antes de comecar (arquivo grande pode levar
minutos, e o access_token do Google expira em ~1h).

Uso:
  python3 upload.py --video "<mp4>" --titulo "..." --descricao-arquivo "<arquivo.txt>" \
    --tags "tag1,tag2,tag3" --privacidade private
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import requests

ENV_PATH = Path(__file__).parent.parent / ".env.local"
CATEGORIA_PEOPLE_BLOGS = "22"


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


def upload(video_path: str, titulo: str, descricao: str, tags: list[str], privacidade: str):
    env = carregar_env()
    token = renovar_token(env)

    body = {
        "snippet": {
            "title": titulo,
            "description": descricao,
            "tags": tags,
            "categoryId": CATEGORIA_PEOPLE_BLOGS,
        },
        "status": {
            "privacyStatus": privacidade,
            "selfDeclaredMadeForKids": False,
        },
    }

    tamanho = Path(video_path).stat().st_size

    resp = requests.post(
        "https://www.googleapis.com/upload/youtube/v3/videos",
        params={"uploadType": "resumable", "part": "snippet,status"},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(tamanho),
        },
        data=json.dumps(body),
    )
    resp.raise_for_status()
    upload_url = resp.headers["Location"]

    print(f"Sessao de upload iniciada. Enviando {tamanho / 1_000_000:.0f}MB...")

    with open(video_path, "rb") as f:
        resp2 = requests.put(
            upload_url,
            data=f,
            headers={
                "Content-Type": "video/mp4",
                "Content-Length": str(tamanho),
            },
        )
    resp2.raise_for_status()
    video = resp2.json()
    return video["id"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--descricao-arquivo", required=True)
    parser.add_argument("--tags", required=True, help="separadas por virgula")
    parser.add_argument("--privacidade", default="private", choices=["private", "unlisted", "public"])
    args = parser.parse_args()

    descricao = Path(args.descricao_arquivo).read_text(encoding="utf-8")
    tags = [t.strip() for t in args.tags.split(",")]

    try:
        video_id = upload(args.video, args.titulo, descricao, tags, args.privacidade)
    except requests.HTTPError as e:
        print(f"Erro no upload: {e}\n{e.response.text}", file=sys.stderr)
        sys.exit(1)

    print(f"Pronto! https://youtu.be/{video_id} (privacidade: {args.privacidade})")
