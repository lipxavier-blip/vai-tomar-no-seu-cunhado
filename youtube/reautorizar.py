#!/usr/bin/env python3
"""
Refaz o OAuth do YouTube e regrava os tokens em .env.local (raiz do projeto).

Por que isso existe: enquanto o app OAuth estiver em modo "Testing" no Google
Cloud, o Google expira o refresh_token em 7 dias. Toda publicacao depois desse
prazo morre com "invalid_grant: Token has been expired or revoked". Rodar este
script resolve na hora. Pra parar de acontecer, publique o app (Google Auth
Platform > Audience > Publish app): em producao o refresh_token nao expira por
tempo.

Uso:
  python3 youtube/reautorizar.py
Abre a URL de consentimento, voce autoriza com vaitomarnoseucunhado@gmail.com,
e o script captura o codigo no localhost e salva os tokens.
"""

import http.server
import json
import socketserver
import threading
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

ENV_PATH = Path("/Users/felipexavier/vai-tomar-no-seu-cunhado/.env.local")
PORTA = 8788
REDIRECT_URI = f"http://localhost:{PORTA}/callback"
SCOPES = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube"

codigo_recebido = {}
recebeu = threading.Event()


def ler_env() -> dict:
    env = {}
    for linha in ENV_PATH.read_text().splitlines():
        linha = linha.strip()
        if "=" in linha and not linha.startswith("#"):
            chave, valor = linha.split("=", 1)
            env[chave] = valor.strip().strip('"')
    return env


def salvar_tokens(env: dict, access_token: str, refresh_token: str):
    """Reescreve so as linhas de token, preservando o resto do arquivo."""
    linhas = ENV_PATH.read_text().splitlines()
    saida = []
    for linha in linhas:
        if linha.startswith("YOUTUBE_ACCESS_TOKEN="):
            saida.append(f"YOUTUBE_ACCESS_TOKEN={access_token}")
        elif linha.startswith("YOUTUBE_REFRESH_TOKEN="):
            saida.append(f"YOUTUBE_REFRESH_TOKEN={refresh_token}")
        else:
            saida.append(linha)
    ENV_PATH.write_text("\n".join(saida) + "\n")


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            codigo_recebido["code"] = params["code"][0]
            corpo = "Autorizado. Pode fechar esta aba e voltar pro terminal."
        else:
            corpo = f"Sem code na resposta: {query}"
        recebeu.set()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(corpo.encode())

    def log_message(self, *args):
        pass  # silencia o log do servidor


def main():
    env = ler_env()
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": env["YOUTUBE_CLIENT_ID"],
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",  # forca vir refresh_token novo
    })

    servidor = socketserver.TCPServer(("", PORTA), Handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()

    print("Abrindo o navegador para autorizar...")
    print("Se nao abrir sozinho, cole esta URL:\n")
    print(auth_url + "\n")
    webbrowser.open(auth_url)

    print("Esperando a autorizacao...")
    if not recebeu.wait(timeout=300):
        print("Timeout de 5 min sem autorizacao. Rode de novo.")
        servidor.shutdown()
        return
    servidor.shutdown()
    if "code" not in codigo_recebido:
        print("Callback chegou sem code. Rode de novo.")
        return

    data = urllib.parse.urlencode({
        "code": codigo_recebido["code"],
        "client_id": env["YOUTUBE_CLIENT_ID"],
        "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req) as resp:
        tokens = json.load(resp)

    if "refresh_token" not in tokens:
        print("A resposta veio sem refresh_token. Revogue o acesso do app na conta Google e rode de novo.")
        print(json.dumps(tokens, indent=2))
        return

    salvar_tokens(env, tokens["access_token"], tokens["refresh_token"])
    print("Tokens salvos em .env.local. Pode rodar o upload de novo.")


if __name__ == "__main__":
    main()
