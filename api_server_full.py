"""
CGC CORE API Server - Production Ready
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os
import sys
from datetime import datetime, timedelta
import mimetypes
import hashlib
import secrets
import re

class AuthSystem:
    """Production-grade authentication"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.users_file = os.path.join(data_dir, 'users.json')
        self.sessions_file = os.path.join(data_dir, 'sessions.json')
        self._init_files()
        self._create_default_admin()
        print("✅ Auth System initialized")
    
    def _init_files(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
    
    def _create_default_admin(self):
        users = self._load_users()
        if 'admin@olympusmont.com' not in users:
            self.create_user('admin@olympusmont.com', 'ChangeMe123!', 'Admin', 'admin')
    
    def _load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_users(self, users):
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _load_sessions(self):
        try:
            with open(self.sessions_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_sessions(self, sessions):
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self) -> str:
        return secrets.token_urlsafe(32)
    
    def _validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_password(self, password: str) -> dict:
        errors = []
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        if not any(c.isupper() for c in password):
            errors.append('Password must contain uppercase letter')
        if not any(c.isdigit() for c in password):
            errors.append('Password must contain number')
        return {'valid': len(errors) == 0, 'errors': errors}
    
    def create_user(self, email: str, password: str, name: str = '', role: str = 'user'):
        email = email.lower().strip()
        
        if not self._validate_email(email):
            return {'success': False, 'error': 'Invalid email format'}
        
        password_check = self._validate_password(password)
        if not password_check['valid']:
            return {'success': False, 'error': password_check['errors'][0]}
        
        users = self._load_users()
        if email in users:
            return {'success': False, 'error': 'User already exists'}
        
        users[email] = {
            'email': email,
            'password_hash': self._hash_password(password),
            'name': name.strip(),
            'role': role,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        self._save_users(users)
        print(f"✅ User created: {email}")
        
        return {
            'success': True,
            'user': {'email': email, 'name': name, 'role': role}
        }
    
    def login(self, email: str, password: str):
        email = email.lower().strip()
        users = self._load_users()
        
        if email not in users:
            return {'success': False, 'error': 'Invalid email or password'}
        
        user = users[email]
        
        if user['password_hash'] != self._hash_password(password):
            return {'success': False, 'error': 'Invalid email or password'}
        
        user['last_login'] = datetime.now().isoformat()
        self._save_users(users)
        
        token = self._generate_token()
        sessions = self._load_sessions()
        
        sessions[token] = {
            'email': email,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat()
        }
        
        self._save_sessions(sessions)
        print(f"✅ Login: {email}")
        
        return {
            'success': True,
            'token': token,
            'user': {
                'email': email,
                'name': user.get('name', ''),
                'role': user.get('role', 'user')
            }
        }
    
    def logout(self, token: str):
        sessions = self._load_sessions()
        if token in sessions:
            del sessions[token]
            self._save_sessions(sessions)
        return {'success': True}

# Import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from discipleai_legal.contract_analyzer_ai import ContractAnalyzerAI

try:
    from cgc_core.core_engine import get_cgc_core
    cgc_core = get_cgc_core()
    CGC_AVAILABLE = True
    print("✅ CGC CORE loaded")
except Exception as e:
    cgc_core = None
    CGC_AVAILABLE = False
    print(f"⚠️  CGC CORE not available: {e}")

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
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/' or path == '/index.html':
            self._serve_file('dist/index.html', 'text/html')
        elif path.startswith('/assets/'):
            file_path = 'dist' + path
            if os.path.exists(file_path):
                mime = mimetypes.guess_type(file_path)[0] or 'text/plain'
                self._serve_file(file_path, mime)
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
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        
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
            self.wfile.write(b'Not found')
    
    def _handle_login(self, data):
        result = auth_system.login(data.get('email', ''), data.get('password', ''))
        self._set_headers(200 if result['success'] else 401)
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_signup(self, data):
        result = auth_system.create_user(
            data.get('email', ''),
            data.get('password', ''),
            data.get('name', '')
        )
        self._set_headers(201 if result['success'] else 400)
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_logout(self, data):
        result = auth_system.logout(data.get('token', ''))
        self._set_headers(200)
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_analyze_contract(self, data):
        text = data.get('text', '')
        if not text:
            self._set_headers(400)
            self.wfile.write(json.dumps({
                'success': False,
                'error': 'No contract text'
            }).encode())
            return
        
        result = contract_analyzer.analyze_contract(
            text,
            metadata={'filename': data.get('filename', 'contract.pdf')}
        )
        
        self._set_headers(200)
        self.wfile.write(json.dumps(result, default=str).encode())
    
    def _handle_metrics(self):
        if CGC_AVAILABLE and cgc_core:
            try:
                metrics = cgc_core.get_real_metrics()
                metrics['cgc_core_active'] = True
                metrics['timestamp'] = datetime.now().isoformat()
            except:
                metrics = self._get_demo_metrics()
        else:
            metrics = self._get_demo_metrics()
        
        self._set_headers(200)
        self.wfile.write(json.dumps(metrics).encode())
    
    def _get_demo_metrics(self):
        return {
            'total_decisions': 0,
            'total_contracts': 0,
            'avg_compliance_score': 0.0,
            'system_health': 0,
            'audit_entries': 0,
            'cgc_core_active': False,
            'demo_mode': True,
            'modules': {}
        }
    
    def _handle_health(self):
        health = {
            'status': 'healthy',
            'cgc_core': CGC_AVAILABLE,
            'auth': True,
            'timestamp': datetime.now().isoformat()
        }
        self._set_headers(200)
        self.wfile.write(json.dumps(health).encode())


def run_server(port=8080):
    port = int(os.environ.get('PORT', port))
    
    server = HTTPServer(('0.0.0.0', port), APIHandler)
    
    print('\n' + '='*60)
    print('🚀 CGC CORE™ SERVER')
    print('='*60)
    print(f'   Server: http://0.0.0.0:{port}')
    print(f'   CGC: {"✅" if CGC_AVAILABLE else "⚠️"}')
    print(f'   Auth: ✅')
    print('='*60 + '\n')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n👋 Server stopped')
        server.shutdown()


if __name__ == '__main__':
    run_server()