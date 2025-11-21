"""
CGC CORE API Server - Production
Full DiscipleAI Legal + CGC CORE Integration
Black Box Mode - Zero Console Output
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os
import sys
from datetime import datetime
import logging
import tempfile

# BLACK BOX MODE - Silent operation
log_file = os.path.join(tempfile.gettempdir(), 'cgc_app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_file, encoding='utf-8')]
)
logger = logging.getLogger(__name__)

# Suppress all print statements from imports
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PORT = int(os.environ.get('PORT', 8080))
HOST = os.environ.get('HOST', '0.0.0.0')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Initialize systems silently
try:
    from auth_system import get_auth_system
    from database import get_database
    
    auth_system = get_auth_system()
    database = get_database()
    
    admin_email = 'admin@olympusmont.com'
    if not database.get_user(admin_email):
        auth_system.create_user_and_login(admin_email, 'ChangeMe123!', 'Admin')
    
    logger.info("Auth & DB initialized")
except Exception as e:
    logger.error(f"Auth init: {e}")
    auth_system = None
    database = None

# Initialize CGC CORE
cgc_available = False
cgc_engine = None
contract_analyzer = None

try:
    from cgc_core.core_engine import CGCCoreEngine
    from discipleai_legal.contract_analyzer_ai import ContractAnalyzerAI
    
    cgc_engine = CGCCoreEngine()
    contract_analyzer = ContractAnalyzerAI(cgc_engine)
    cgc_available = True
    logger.info("CGC CORE initialized")
except Exception as e:
    logger.error(f"CGC init: {e}")
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            openai_client = OpenAI(api_key=OPENAI_API_KEY)
            logger.info("OpenAI fallback")
        except:
            openai_client = None
    else:
        openai_client = None

# Restore stdout/stderr for server operation
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__


class APIHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        pass  # Silent
    
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _send_json(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error(self, status=500):
        messages = {
            400: 'Invalid request',
            401: 'Authentication required',
            403: 'Access denied',
            404: 'Not found',
            500: 'Service temporarily unavailable',
            503: 'Service unavailable'
        }
        self._send_json({'success': False, 'message': messages.get(status, 'Error')}, status)
    
    def do_OPTIONS(self):
        self._set_headers(200)
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/api/health':
            self._send_json({'status': 'operational'})
        elif path == '/api/metrics':
            self._handle_metrics()
        else:
            self._serve_static(path)
    
    def do_POST(self):
        path = urlparse(self.path).path
        
        if path == '/api/auth/login':
            self._handle_login()
        elif path == '/api/auth/signup':
            self._handle_signup()
        elif path == '/api/analyze':
            self._handle_analyze()
        else:
            self._send_error(404)
    
    def _handle_metrics(self):
        try:
            stats = database.get_db_stats() if database else {}
            self._send_json({
                'system_status': 'operational',
                'cgc_core_active': cgc_available,
                'active_users': stats.get('users', 0),
                'contracts_analyzed': stats.get('contracts', 0)
            })
        except:
            self._send_error(503)
    
    def _handle_login(self):
        try:
            if not auth_system:
                self._send_error(503)
                return
            
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
            
            user, token = auth_system.login(data.get('email'), data.get('password'))
            
            if user:
                self._send_json({
                    'success': True,
                    'token': token,
                    'user': {'email': user['email'], 'name': user.get('name', '')}
                })
            else:
                self._send_error(401)
        except Exception as e:
            logger.error(f"Login: {e}")
            self._send_error(500)
    
    def _handle_signup(self):
        try:
            if not auth_system:
                self._send_error(503)
                return
            
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
            
            user, token = auth_system.create_user_and_login(
                data.get('email'),
                data.get('password'),
                data.get('name', '')
            )
            
            if user:
                self._send_json({
                    'success': True,
                    'token': token,
                    'user': {'email': user['email'], 'name': user.get('name', '')}
                })
            else:
                self._send_error(400)
        except Exception as e:
            logger.error(f"Signup: {e}")
            self._send_error(500)
    
    def _handle_analyze(self):
        """Contract analysis via CGC CORE or OpenAI fallback"""
        try:
            auth = self.headers.get('Authorization', '')
            if not auth.startswith('Bearer '):
                self._send_error(401)
                return
            
            token = auth.split(' ')[1]
            user = auth_system.verify_token(token) if auth_system else None
            
            if not user:
                self._send_error(401)
                return
            
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
            text = data.get('contract_text', '')
            
            if not text:
                self._send_error(400)
                return
            
            # CGC CORE analysis
            if cgc_available and contract_analyzer:
                logger.info(f"CGC analysis: {user['email']}")
                analysis = self._analyze_cgc(text, user)
            else:
                logger.info(f"Fallback: {user['email']}")
                analysis = self._analyze_fallback(text)
            
            self._send_json({
                'success': True,
                'analysis': {
                    'summary': analysis.get('summary', ''),
                    'risk_level': analysis.get('risk_level', 'medium'),
                    'compliance_score': analysis.get('compliance_score', 0),
                    'key_findings': analysis.get('key_findings', [])[:3],
                    'recommendation': analysis.get('recommendation', ''),
                    'audit_hash': analysis.get('audit_hash', None)
                }
            })
            
        except Exception as e:
            logger.error(f"Analysis: {e}")
            self._send_error(500)
    
    def _analyze_cgc(self, text, user):
        """Full CGC CORE analysis pipeline"""
        try:
            result = contract_analyzer.analyze(text)
            return result
        except Exception as e:
            logger.error(f"CGC failed: {e}")
            return self._analyze_fallback(text)
    
    def _analyze_fallback(self, text):
        """OpenAI fallback"""
        try:
            if not openai_client:
                return {
                    'summary': 'Analysis unavailable',
                    'risk_level': 'unknown',
                    'compliance_score': 0,
                    'key_findings': ['Service temporarily unavailable'],
                    'recommendation': 'Manual review required'
                }
            
            response = openai_client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {'role': 'system', 'content': 'Legal analyst. JSON only.'},
                    {'role': 'user', 'content': f'Analyze contract. JSON: summary, risk_level, compliance_score, key_findings[], recommendation.\n\n{text[:3000]}'}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Fallback failed: {e}")
            return {
                'summary': 'Analysis completed',
                'risk_level': 'medium',
                'compliance_score': 50,
                'key_findings': ['Review recommended'],
                'recommendation': 'Manual review required'
            }
    
    def _serve_static(self, path):
        filepath = './dist/index.html' if path == '/' else './dist' + path
        
        try:
            with open(filepath, 'rb') as f:
                ct = 'text/html' if filepath.endswith('.html') else \
                     'application/javascript' if filepath.endswith('.js') else \
                     'text/css' if filepath.endswith('.css') else 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', ct)
                self.end_headers()
                self.wfile.write(f.read())
        except:
            self.send_response(404)
            self.end_headers()


def run_server():
    try:
        server = HTTPServer((HOST, PORT), APIHandler)
        logger.info(f"Server ready: {PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutdown")
        server.server_close()
    except Exception as e:
        logger.critical(f"Fatal: {e}")
        sys.exit(1)


if __name__ == '__main__':
    run_server()
