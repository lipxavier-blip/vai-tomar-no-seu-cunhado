"""Serve uma página de aprovação e grava o que o Felipe salvar.
Uso: python3 servidor_aprovacao.py <pagina.html> <saida.json> [porta]"""
import http.server, json, os, sys
page, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
port = int(sys.argv[3]) if len(sys.argv) > 3 else 8790

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
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
