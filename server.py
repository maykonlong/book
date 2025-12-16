
import http.server
import socketserver
import json
import os
import subprocess
import sys

PORT = 8000
PASSWORD = "@Rainha0204"

class BookHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # auth
                if data.get('password') != PASSWORD:
                    self.send_response(403)
                    self.end_headers()
                    self.wfile.write(b'Senha incorreta')
                    return

                filepath = data.get('filepath')
                content = data.get('content')
                
                # security check: prevent going up directories
                if '..' in filepath or not filepath.endswith('.md'):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Arquivo invalido')
                    return

                # Save file
                full_path = os.path.join(os.getcwd(), filepath)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Update JS content (run powershell script)
                # We assume powershell is available since user used it before
                subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "generate_book_content.ps1"], check=True)

                # Git Operations
                subprocess.run(["git", "add", filepath], check=True)
                subprocess.run(["git", "add", "js/book-content-*.js"], check=True) # Add generated JS files
                subprocess.run(["git", "commit", "-m", f"edit: {filepath} via web editor"], check=True)
                subprocess.run(["git", "push"], check=True)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

            except Exception as e:
                print(f"Error: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            self.send_error(404)

print(f"Servidor rodando em http://localhost:{PORT}")
print(f"Para acessar de outros dispositivos, precisaremos de um tunel (ex: ngrok) ou abrir a porta no firewall.")

with socketserver.TCPServer(("", PORT), BookHandler) as httpd:
    httpd.serve_forever()
