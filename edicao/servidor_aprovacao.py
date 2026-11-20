"""Serve uma página de aprovação e grava o que o Felipe salvar.
Uso: python3 servidor_aprovacao.py <pagina.html> <saida.json> [porta]"""
import http.server, json, mimetypes, os, sys, urllib.parse
page, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
port = int(sys.argv[3]) if len(sys.argv) > 3 else 8790

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # arquivos ao lado da página (áudio das prévias etc.); "/" é a página
        rel = urllib.parse.unquote(self.path.split('?')[0]).lstrip('/')
        f = os.path.realpath(os.path.join(os.path.dirname(page), rel))
        if rel and f.startswith(os.path.dirname(page) + os.sep) and os.path.isfile(f):
            body = open(f, 'rb').read(); ct = mimetypes.guess_type(f)[0] or 'application/octet-stream'
            rg = self.headers.get('Range')   # pedido parcial: o player só pula pro meio de um mp3 longo com isso
            if rg and rg.startswith('bytes='):
                a, _, b = rg[6:].partition('-'); a = int(a or 0); b = int(b) if b else len(body) - 1
                part = body[a:b + 1]; self.send_response(206)
                self.send_header('Content-Range', f'bytes {a}-{a + len(part) - 1}/{len(body)}')
                self.send_header('Content-Type', ct); self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Content-Length', str(len(part))); self.end_headers(); self.wfile.write(part); return
            self.send_response(200); self.send_header('Content-Type', ct); self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
        body = open(page, 'rb').read()
        self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        if self.path != '/save': self.send_response(404); self.end_headers(); return
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        with open(out, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
        print('SALVO', out, flush=True)
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self, *a): pass

http.server.HTTPServer(('127.0.0.1', port), H).serve_forever()
