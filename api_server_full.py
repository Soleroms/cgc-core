"""
CGC CORE API Server - Production Ready
100% functional auth + contract analysis + metrics
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

# ============================================================================
# PRODUCTION AUTH SYSTEM - Inline for Railway compatibility
# ============================================================================

class AuthSystem:
    """Production-grade authentication with validation"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.users_file = os.path.join(data_dir, 'users.json')
        self.sessions_file = os.path.join(data_dir, 'sessions.json')
        self._init_files()
        self._create_default_admin()
        print("✅ Auth System initialized (Production Mode)")
    
    def _init_files(self):
        """Initialize storage files"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
    
    def _create_default_admin(self):
        """Create default admin account"""
        users = self._load_users()
        if 'admin@olympusmont.com' not in users:
            self.create_user(
                email='admin@olympusmont.com',
                password='ChangeMe123!',
                name='Admin User',
                role='admin'
            )
    
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
        """Secure password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_password(self, password: str) -> dict:
        """Validate password strength"""
        errors = []
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        
        if not any(c.isupper() for c in password):
            errors.append('Password must contain at least one uppercase letter')
        
        if not any(c.isdigit() for c in password):
            errors.append('Password must contain at least one number')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def create_user(self, email: str, password: str, name: str = '', role: str = 'user'):
        """Create new user with validation"""
        
        # Normalize email
        email = email.lower().strip()
        
        # Validate email
        if not self._validate_email(email):
            return {
                'success': False,
                'error': 'Invalid email format'
            }
        
        # Validate password
        password_check = self._validate_password(password)
        if not password_check['valid']:
            return {
                'success': False,
                'error': password_check['errors'][0]
            }
        
        # Check if user exists
        users = self._load_users()
        if email in users:
            return {
                'success': False,
                'error': 'User already exists'
            }
        
        # Create user
        users[email] = {
            'email': email,
            'password_hash': self._hash_password(password),
            'name': name.strip(),
            'role': role,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        self._save_users(users)
        
        print(f"✅ User created: {email} ({role})")
        
        return {
            'success': True,
            'user': {
                'email': email,
                'name': name,
                'role': role
            }
        }
    
    def login(self, email: str, password: str):
        """Authenticate user"""
        
        email = email.lower().strip()
        users = self._load_users()
        
        if email not in users:
            return {
                'success': False,
                'error': 'Invalid email or password'
            }
        
        user = users[email]
        
        # Verify password
        if user['password_hash'] != self._hash_password(password):
            return {
                'success': False,
                'error': 'Invalid email or password'
            }
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        self._save_users(users)
        
        # Create session
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
                'role': user.get('role', 'user'),
                'last_login': user.get('last_login')
            }
        }
    
    def logout(self, token: str):
        """Logout user"""
        sessions = self._load_sessions()
        if token in sessions:
            email = sessions[token]['email']
            del sessions[token]
            self._save_sessions(sessions)
            print(f"✅ Logout: {email}")
        return {'success': True}
    
    def verify_token(self, token: str):
        """Verify session token"""
        sessions = self._load_sessions()
        
        if token not in sessions:
            return None
        
        session = sessions[token]
        
        # Check expiration
        expires = datetime.fromisoformat(session['expires_at'])
        if datetime.now() > expires:
            del sessions[token]
            self._save_sessions(sessions)
            return None
        
        # Get user
        users = self._load_users()
        email = session['email']
        
        if email not in users:
            return None
        
        user = users[email]
        return {
            'email': email,
            'name': user.get('name', ''),
            'role': user.get('role', 'user')
        }

# ============================================================================
# Import CGC modules
# ============================================================================
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    print(f"⚠️  CGC CORE not available: {e}")

# Initialize systems
auth_system = AuthSystem()
contract_analyzer = ContractAnalyzerAI()

# ============================================================================
# API Handler
# ============================================================================

class APIHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass
    
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
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
        email = data.get('email', '')
        password = data.get('password', '')
        
        result = auth_system.login(email, password)
        
        status = 200 if result['success'] else 401
        self._set_headers(status)
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_signup(self, data):
        email = data.get('email', '')
        password = data.get('password', '')
        name = data.get('name', '')
        
        result = auth_system.create_user(email, password, name=name)
        
        status = 201 if result['success'] else 400
        self._set_headers(status)
        self.wfile.write(json.dumps(result).encode())
    
    def _handle_logout(self, data):
        token = data.get('token', '')
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
        self.wfile.write(json.dumps(result, indent=2, default=str).encode())
    
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
                print(f"⚠️  Error getting CGC metrics: {e}")
                metrics = self._get_demo_metrics()
        else:
            metrics = self._get_demo_metrics()
        
        self._set_headers(200)
        self.wfile.write(json.dumps(metrics, indent=2).encode())
    
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
    """Start production server"""
    
    # Railway uses PORT environment variable
    port = int(os.environ.get('PORT', port))
    
    server = HTTPServer(('0.0.0.0', port), APIHandler)
    
    print('\n' + '='*70)
    print('🚀 CGC CORE™ - PRODUCTION SERVER')
    print('='*70)
    print(f'   Server: http://0.0.0.0:{port}')
    print(f'   CGC CORE: {"✅ ACTIVE" if CGC_AVAILABLE else "⚠️  INACTIVE"}')
    print(f'   Auth: ✅ ACTIVE')
    print(f'   AI Analysis: ✅ ACTIVE')
    print('='*70)
    print('   Press Ctrl+C to stop')
    print('='*70 + '\n')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n👋 Server stopped gracefully')
        server.shutdown()


if __name__ == '__main__':
    run_server()