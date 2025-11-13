"""
CGC Core Full Stack API Server
Serves both API and React frontend
OlympusMont Systems LLC
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get('PORT', 8000))

sys.path.insert(0, os.path.abspath('cgc_core'))
sys.path.insert(0, os.path.abspath('discipleai_legal'))

try:
    from cgc_core_integration import create_cgc_core
    from contract_analyzer import ContractAnalyzer
    CGC_AVAILABLE = True
    cgc = create_cgc_core({'confidence_threshold': 0.85})
    contract_analyzer = ContractAnalyzer()
except ImportError as e:
    print(f"Warning: CGC modules not available: {e}")
    CGC_AVAILABLE = False
    cgc = None
    contract_analyzer = None


class FullStackHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
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
                    metrics = cgc.cgc.get_metrics()
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
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/decision':
            self._handle_decision()
        elif path == '/api/analyze-contract':
            self._handle_contract_analysis()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def _handle_decision(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            if not CGC_AVAILABLE or not cgc:
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    'status': 'demo_mode',
                    'message': 'CGC Core not available - this is a demo response'
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
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def _handle_contract_analysis(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            if not contract_analyzer:
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    'status': 'demo_mode',
                    'message': 'Contract Analyzer not available - this is a demo response'
                }).encode())
                return

            contract_text = data.get('contract_text', '')
            result = contract_analyzer.analyze(contract_text)

            self._set_headers(200)
            self.wfile.write(json.dumps(result, indent=2).encode())

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def _serve_static_file(self, path):
        # Placeholder: implement static file serving from ./dist if needed
        self._set_headers(404)
        self.wfile.write(json.dumps({'error': 'Static file not found'}).encode())


if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, FullStackHandler)
    print(f"Starting server on port {PORT}...")
    httpd.serve_forever()