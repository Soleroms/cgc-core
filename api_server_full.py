"""
CGC Core Full Stack API Server
Serves both API and React frontend
OlympusMont Systems LLC
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys
from urllib.parse import urlparse
import mimetypes # Necesario para servir archivos estáticos correctamente

PORT = int(os.environ.get('PORT', 8000))
STATIC_DIR = 'dist'


# Add after existing imports
import sys
sys.path.insert(0, '.')
from auth_system import auth
# --- Módulos Placeholder para entrono local ---

class PlaceholderCGC:
    """Simulación del CGC Core."""
    def create_cgc_core(self, config):
        return self
    def execute_decision(self, module, action, input_data, context):
        return {
            'status': 'success',
            'decision': 'DEMO_APPROVED',
            'confidence': 0.0,
            'details': f"Processed action {action} in demo mode"
        }
    def get_metrics(self):
        return {
            'requests_handled': 0,
            'avg_latency_ms': 0,
            'core_version': 'DEMO-1.0.0'
        }

class PlaceholderContractAnalyzer:
    """Simulación del Analizador de Contratos."""
    def analyze(self, contract_text):
        return {
            'summary': f"Demo analysis complete. Length: {len(contract_text)} chars.",
            'risk_level': 'UNKNOWN (Demo)',
            'issues_found': 0
        }

# --- Inicialización de Módulos ---
sys.path.insert(0, os.path.abspath('cgc_core'))
sys.path.insert(0, os.path.abspath('discipleai_legal'))

try:
    # Intenta usar los módulos reales
    from cgc_core_integration import create_cgc_core
    from contract_analyzer import ContractAnalyzer
    CGC_AVAILABLE = True
    cgc = create_cgc_core({'confidence_threshold': 0.85})
    contract_analyzer = ContractAnalyzer()
except ImportError as e:
    # Usa los placeholders si los módulos no están disponibles
    print(f"Warning: CGC modules not available: {e}. Running with placeholders.")
    CGC_AVAILABLE = False
    cgc = PlaceholderCGC().create_cgc_core({})
    # Try to import AI analyzer
try:
    import sys
    sys.path.insert(0, 'discipleai_legal')
    from contract_analyzer_ai import AIContractAnalyzer
    contract_analyzer = AIContractAnalyzer()
    print("✅ AI Contract Analyzer loaded")
except Exception as e:
    print(f"⚠️  Using placeholder analyzer: {e}")
    contract_analyzer = PlaceholderContractAnalyzer()


class FullStackHandler(BaseHTTPRequestHandler):
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
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/health':
            self._set_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            return

        if path.startswith('/api/'):
            self._handle_api_get(path)
        else:
            self._serve_static_file(path)

def _handle_auth_login(self):
        """Handle login"""
        try:
            data = self._get_post_data()
        except ValueError:
            return
        
        email = data.get('email')
        password = data.get('password')
        ip = self.client_address[0]
        
        result = auth.login(email, password, ip)
        
        self._set_headers(200 if result['success'] else 401)
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_auth_signup(self):
        """Handle signup"""
        try:
            data = self._get_post_data()
        except ValueError:
            return
        
        email = data.get('email')
        password = data.get('password')
        
        result = auth.create_user(email, password, role='user', created_by='self-signup')
        
        self._set_headers(200 if result['success'] else 400)
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_auth_users(self):
        """List users (admin only)"""
        token = self.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth.verify_token(token)
        
        if not user:
            self._set_headers(401)
            self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
            return
        
        result = auth.list_users(user['role'])
        
        self._set_headers(200 if result['success'] else 403)
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_auth_stats(self):
        """Get auth stats"""
        stats = auth.get_stats()
        self._set_headers(200)
        self.wfile.write(json.dumps(stats).encode())
    def _handle_api_get(self, path):
        if path == '/api/health':
            self._set_headers()
            response = {
                'status': 'healthy',
                'service': 'CGC Core Full Stack',
                'version': '2.1.4',
                'cgc_loaded': CGC_AVAILABLE,
                'modules': {
                    'cgc_core': CGC_AVAILABLE,
                    'contract_analyzer': contract_analyzer is not None
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode())

        elif path == '/api/metrics':
            self._set_headers()
            if cgc and CGC_AVAILABLE:
                try:
                    # Nota: La llamada original 'cgc.cgc.get_metrics()' parecía incorrecta.
                    # Se asume que el objeto 'cgc' ya es la instancia del core.
                    metrics = cgc.get_metrics()
                    self.wfile.write(json.dumps(metrics, indent=2).encode())
                except Exception as e:
                    self._set_headers(500)
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
            else:
                self.wfile.write(json.dumps({
                    'status': 'demo_mode',
                    'message': 'CGC Core not loaded - running in demo mode'
                }).encode())

        elif path == '/api/status':
            self._set_headers()
            status = {
                'cgc_core': 'active' if CGC_AVAILABLE else 'unavailable',
                'contract_analyzer': 'active' if contract_analyzer else 'unavailable',
                'uptime': 'active'
            }
            self.wfile.write(json.dumps(status, indent=2).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

   def do_POST(self):
        """Handle POST requests"""
        
        # Auth endpoints
        if self.path == '/api/auth/login':
            return self._handle_auth_login()
        
        if self.path == '/api/auth/signup':
            return self._handle_auth_signup()
        
        if self.path == '/api/auth/users':
            return self._handle_auth_users()
        
        # Existing endpoints...
        if self.path == '/api/analyze-contract':
            return self._handle_contract_analysis()
        
        # ... rest of existing code

    def _get_post_data(self):
        """Helper para obtener y decodificar el cuerpo de la petición POST."""
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        except (KeyError, ValueError, AttributeError):
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Invalid Content-Length or JSON'}).encode())
            # Es importante elevar una excepción para que las funciones _handle_... no continúen
            raise ValueError("Invalid POST data")

    def _handle_decision(self):
        try:
            data = self._get_post_data()
        except ValueError:
            return

        try:
            if not CGC_AVAILABLE or not cgc:
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    'status': 'demo_mode',
                    'message': 'CGC Core not available - this is a demo response',
                    'input_received': data
                }).encode())
                return

            result = cgc.execute_decision(
                module=data.get('module', 'api'),
                action=data.get('action', 'test'),
                input_data=data.get('input_data', {}),
                context=data.get('context', {})
            )

            self._set_headers(200)
            self.wfile.write(json.dumps(result, indent=2, default=str).encode())

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': f"Decision execution failed: {str(e)}"}).encode())

    def _handle_contract_analysis(self):
        try:
            data = self._get_post_data()
        except ValueError:
            return

        try:
            contract_text = data.get('contract_text', '')

            if not contract_analyzer:
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    'status': 'demo_mode',
                    'message': 'Contract Analyzer not available or no text provided',
                    'text_length': len(contract_text)
                }).encode())
                return

            result = contract_analyzer.analyze(contract_text)

            self._set_headers(200)
            self.wfile.write(json.dumps(result, indent=2).encode())

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': f"Analysis execution failed: {str(e)}"}).encode())

    def _serve_static_file(self, path):
        """Sirve archivos estáticos desde la carpeta 'dist'."""
        if path == '/':
            path = '/index.html'

        file_path = os.path.join(STATIC_DIR, path[1:])

        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'

            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            # Fallback para SPAs (React) a index.html
            try:
                with open(os.path.join(STATIC_DIR, 'index.html'), 'rb') as f:
                    content = f.read()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'File not found'}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': f"Server error while serving static file: {str(e)}"}).encode())


if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, FullStackHandler)
    print(f"Starting server on port {PORT}...")
    httpd.serve_forever()