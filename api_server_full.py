"""
API Server with CGC CORE Integration
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os
import sys
from datetime import datetime
import mimetypes

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import systems
from auth_system import AuthSystem
from discipleai_legal.contract_analyzer_ai import ContractAnalyzerAI

# Initialize CGC CORE
try:
    from cgc_core.core_engine import get_cgc_core
    cgc_core = get_cgc_core()
    CGC_AVAILABLE = True
    print("✅ CGC CORE loaded and operational")
except Exception as e:
    cgc_core = None
    CGC_AVAILABLE = False
    print(f"⚠️ CGC CORE not available: {e}")

# Initialize
auth_system = AuthSystem()
contract_analyzer = ContractAnalyzerAI()


class APIHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        pass
    
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/' or path == '/index.html':
            self._serve_file('dist/index.html', 'text/html')
        elif path.startswith('/assets/'):
            file_path = 'dist' + path
            if os.path.exists(file_path):
                mime_type = mimetypes.guess_type(file_path)[0] or 'text/plain'
                self._serve_file(file_path, mime_type)
            else:
                self._set_headers(404)
                self.wfile.write(b'Not found')
        elif path == '/api/metrics':
            self._handle_metrics()
        elif path == '/api/health':
            self._handle_health()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def do_POST(self):
        path = self.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode()) if body else {}
        except:
            data = {}
        
        if path == '/api/auth/login':
            self._handle_login(data)
        elif path == '/api/auth/signup':
            self._handle_signup(data)
        elif path == '/api/auth/logout':
            self._handle_logout(data)
        elif path == '/api/analyze-contract':
            self._handle_analyze_contract(data)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def _serve_file(self, filepath, content_type):
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self._set_headers(200, content_type)
            self.wfile.write(content)
        except FileNotFoundError:
            self._set_headers(404)
            self.wfile.write(b'File not found')
    
    def _handle_login(self, data):
        email = data.get('email')
        password = data.get('password')
        result = auth_system.login(email, password)
        
        if result['success']:
            self._set_headers(200)
        else:
            self._set_headers(401)
        
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_signup(self, data):
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', '')
        result = auth_system.create_user(email, password, name=name)
        
        if result['success']:
            self._set_headers(201)
        else:
            self._set_headers(400)
        
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_logout(self, data):
        token = data.get('token')
        result = auth_system.logout(token)
        self._set_headers(200)
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_analyze_contract(self, data):
        contract_text = data.get('text', '')
        filename = data.get('filename', 'contract.pdf')
        
        if not contract_text:
            self._set_headers(400)
            self.wfile.write(json.dumps({
                'success': False,
                'error': 'No contract text provided'
            }).encode())
            return
        
        result = contract_analyzer.analyze_contract(
            contract_text,
            metadata={'filename': filename}
        )
        
        self._set_headers(200)
        self.wfile.write(json.dumps(result, indent=2).encode())
    
    def _handle_metrics(self):
        if CGC_AVAILABLE and cgc_core:
            try:
                real_metrics = cgc_core.get_real_metrics()
                
                metrics = {
                    'total_decisions': real_metrics['total_decisions'],
                    'total_contracts': real_metrics['total_contracts'],
                    'avg_compliance_score': real_metrics['avg_compliance_score'],
                    'system_health': real_metrics['system_health'],
                    'audit_entries': real_metrics['audit_entries'],
                    'modules': real_metrics['modules'],
                    'cgc_core_active': True,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                print(f"Error getting CGC metrics: {e}")
                metrics = self._get_demo_metrics()
        else:
            metrics = self._get_demo_metrics()
        
        self._set_headers(200)
        self.wfile.write(json.dumps(metrics, indent=2).encode())
    
    def _get_demo_metrics(self):
        return {
            'total_decisions': 12400000,
            'total_contracts': 1547832,
            'avg_compliance_score': 96.8,
            'system_health': 98.0,
            'audit_entries': 2847391,
            'cgc_core_active': False,
            'demo_mode': True
        }
    
    def _handle_health(self):
        health = {
            'status': 'healthy',
            'cgc_core': CGC_AVAILABLE,
            'timestamp': datetime.now().isoformat()
        }
        self._set_headers(200)
        self.wfile.write(json.dumps(health).encode())


def run_server(port=8000):
    server = HTTPServer(('', port), APIHandler)
    print(f'\n✅ Server running on http://localhost:{port}')
    print(f'   CGC CORE: {"ACTIVE" if CGC_AVAILABLE else "INACTIVE"}')
    print(f'   Press Ctrl+C to stop\n')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n👋 Server stopped')
        server.shutdown()


if __name__ == '__main__':
    run_server(8080)