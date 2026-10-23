"""Local-only standard-library API with a small static browser demo.
Not secured for public deployment; do not expose to the internet.
"""
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from .engine import evaluate, load_records
ROOT=Path(__file__).resolve().parents[2]
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/","/index.html"):
            content=(ROOT/"web"/"index.html").read_bytes()
            self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8");self.send_header("Content-Length",str(len(content)));self.end_headers();self.wfile.write(content)
        elif self.path=="/health": self._json(200,{"status":"ok","mode":"synthetic-demo"})
        else: self._json(404,{"error":"not found"})
    def _json(self,code,obj):
        payload=json.dumps(obj).encode("utf-8");self.send_response(code);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(payload)));self.end_headers();self.wfile.write(payload)
    def do_POST(self):
        if self.path!="/evaluate":return self._json(404,{"error":"not found"})
        try:
            n=int(self.headers.get("Content-Length","0"))
            if n<1 or n>20000: return self._json(413,{"error":"body must be 1-20000 bytes"})
            data=json.loads(self.rfile.read(n))
            if not isinstance(data,dict): raise ValueError("proposal must be an object")
            return self._json(200,evaluate(data,load_records()))
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as e:
            return self._json(400,{"error":str(e)})
def main():
    server=ThreadingHTTPServer(("127.0.0.1",8765),Handler)
    print("LOCAL SYNTHETIC DEMO http://127.0.0.1:8765 (Ctrl+C to stop)")
    try:server.serve_forever()
    except KeyboardInterrupt: pass
    finally:server.server_close()
if __name__=="__main__":main()
