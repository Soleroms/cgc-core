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
import mimetypes

PORT = int(os.environ.get('PORT', 8000))
STATIC_DIR = os.environ.get('STATIC_DIR', 'dist')

# --- Intento de cargar sistema de auth (si existe) ---
try:
    # Si tienes auth_system.py en la raíz con objeto 'auth'
    sys.path.insert(0, '.')
    from auth_system import auth
    AUTH_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Auth system not available: {e}")
    auth = None
    AUTH_AVAILABLE = False

# --- Placeholder CGC y Contract Analyzer (modo demo) ---
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

# --- Intento de cargar módulos reales (si existen) ---
CGC_AVAILABLE = False
cgc = None
contract_analyzer = None

# Añadir rutas donde podrían estar tus paquetes locales
sys.path.insert(0, os.path.abspath('cgc_core'))
sys.path.insert(0, os.path.abspath('discipleai_legal'))

try:
    from cgc_core_integration import create_cgc_core
    from contract_analyzer import ContractAnalyzer
    cgc = create_cgc_core({'confidence_threshold': 0.85})
    contract_analyzer = ContractAnalyzer()
    CGC_AVAILABLE = True
    print("✅ CGC Core loaded")
except Exception as e:
    print(f"Warning: CGC modules not available: {e}. Running with placeholders.")
    cgc = PlaceholderCGC().create_cgc_core({})

# Intento de cargar analizador AI (si existe)
try:
    sys.path.insert(0, os.path.abspath('discipleai_legal'))
    from contract_analyzer_ai import AIContractAnalyzer
    contract_analyzer = AIContractAnalyzer()
    print("✅ AI Contract Analyzer loaded")
except Exception as e:
    if contract_analyzer is None:
        print(f"⚠️  Using placeholder analyzer: {e}")
        contract_analyzer = PlaceholderContractAnalyzer()


class FullStackHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        # CORS - ajustar si necesitas restringir orígenes
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Health endpoint simple (no auth)
        if path == '/health':
            self._set_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            return

        # API routes
        if path.startswith('/api/'):
            return self._handle_api_get(path)

        # Static / frontend
        return self._serve_static_file(path)

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
            self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
            return

        if path == '/api/metrics':
            self._set_headers()
            if cgc and CGC_AVAILABLE:
                try:
                    metrics = cgc.get_metrics()
                    self.wfile.write(json.dumps(metrics, indent=2).encode('utf-8'))
                except Exception as e:
                    self._set_headers(500)
                    self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({
                    'status': 'demo_mode',
                    'message': 'CGC Core not loaded - running in demo mode'
                }).encode('utf-8'))
            return

        if path == '/api/status':
            self._set_headers()
            status = {
                'cgc_core': 'active' if CGC_AVAILABLE else 'unavailable',
                'contract_analyzer': 'active' if contract_analyzer else 'unavailable',
                'uptime': 'active'
            }
            self.wfile.write(json.dumps(status, indent=2).encode('utf-8'))
            return

        # Unknown API
        self._set_headers(404)
        self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def do_POST(self):
        path = self.path

        # Auth endpoints
        if path == '/api/auth/login':
            return self._handle_auth_login()

        if path == '/api/auth/signup':
            return self._handle_auth_signup()

        if path == '/api/auth/users':
            return self._handle_auth_users()

        if path == '/api/auth/stats':
            return self._handle_auth_stats()

        # Decision endpoint
        if path == '/api/decision':
            return self._handle_decision()

        # Contract analysis
        if path == '/api/analyze-contract':
            return self._handle_contract_analysis()

        # Default: not found
        self._set_headers(404)
        self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def _handle_auth_login(self):
        """Handle login"""
        if not AUTH_AVAILABLE or auth is None:
            self._set_headers(503)
            self.wfile.write(json.dumps({'error': 'Auth system unavailable'}).encode('utf-8'))
            return

        try:
            data = self._get_post_data()
        except ValueError:
            return

        email = data.get('email')
        password = data.get('password')
        ip = self.client_address[0] if self.client_address else None

        try:
            result = auth.login(email, password, ip)
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': f'Auth login failed: {str(e)}'}).encode('utf-8'))
            return

        self._set_headers(200 if result.get('success') else 401)
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def _handle_auth_signup(self):
        """Handle signup"""
        if not AUTH_AVAILABLE or auth is None:
            self._set_headers(503)
            self.wfile.write(json.dumps({'error': 'Auth system unavailable'}).encode('utf-8'))
            return

        try:
            data = self._get_post_data()
        except ValueError:
            return

        email = data.get('email')
        password = data.get('password')

        try:
            result = auth.create_user(email, password, role='user', created_by='self-signup')
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': f'Auth signup failed: {str(e)}'}).encode('utf-8'))
            return

        self._set_headers(200 if result.get('success') else 400)
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def _handle_auth_users(self):
        """List users (admin only)"""
        if not AUTH_AVAILABLE or auth is None:
            self._set_headers(503)
            self.wfile.write(json.dumps({'error': 'Auth system unavailable'}).encode('utf-8'))
            return

        token = self.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            user = auth.verify_token(token)
        except Exception as e:
            self._set_headers(401)
            self.wfile.write(json.dumps({'error': f'Invalid token: {str(e)}'}).encode('utf-8'))
            return

        if not user:
            self._set_headers(401)
            self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode('utf-8'))
            return

        try:
            result = auth.list_users(user.get('role'))
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': f'Failed to list users: {str(e)}'}).encode('utf-8'))
            return

        self._set_headers(200 if result.get('success') else 403)
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def _handle_auth_stats(self):
        """Get auth stats"""
        if not AUTH_AVAILABLE or auth is None:
            self._set_headers(503)
            self.wfile.write(json.dumps({'error': 'Auth system unavailable'}).encode('utf-8'))
            return

        try:
            stats = auth.get_stats()
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': f'Failed to get stats: {str(e)}'}).encode('utf-8'))
            return

        self._set_headers(200)
        self.wfile.write(json.dumps(stats).encode('utf-8'))

    def _get_post_data(self):
        """Helper para obtener y decodificar el cuerpo de la petición POST."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Empty body or missing Content-Length'}).encode('utf-8'))
                raise ValueError("Invalid POST data: empty")
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        except (ValueError, json.JSONDecodeError) as e:
            # Already sent a 400 above in some cases; ensure response
            try:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Invalid JSON or Content-Length'}).encode('utf-8'))
            except Exception:
                pass
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
                }).encode('utf-8'))
                return

            result = cgc.execute_decision(
                module=data.get('module', 'api'),
                action=data.get('action', 'test'),
                input_data=data.get('input_data', {}),
                context=data.get('context', {})
            )

            self._set_headers(200)
            self.wfile.write(json.dumps(result, indent=2, default=str).encode('utf-8'))

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': f"Decision execution failed: {str(e)}"}).encode('utf-8'))

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
                }).encode('utf-8'))
                return

            result = contract_analyzer.analyze(contract_text)

            self._set_headers(200)
            self.wfile.write(json.dumps(result, indent=2).encode('utf-8'))

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': f"Analysis execution failed: {str(e)}"}).encode('utf-8'))

    def _serve_static_file(self, path):
        """Sirve archivos estáticos desde la carpeta STATIC_DIR."""
        if path == '/' or path == '':
            path = '/index.html'

        # Evitar path traversal
        safe_path = os.path.normpath(path).lstrip(os.sep)
        file_path = os.path.join(STATIC_DIR, safe_path)

        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'

            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            # Fallback SPA to index.html
            try:
                index_path = os.path.join(STATIC_DIR, 'index.html')
                with open(index_path, 'rb') as f:
                    content = f.read()

                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'File not found'}).encode('utf-8'))
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': f"Server error while serving static file: {str(e)}"}).encode('utf-8'))


if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, FullStackHandler)
    print(f"Starting server on port {PORT} (STATIC_DIR={STATIC_DIR})...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server...")
        httpd.server_close()
