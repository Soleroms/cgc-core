"""
Authentication & Security System
OlympusMont Systems LLC - CGC CORE™
"""

import json
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import os

try:
    import bcrypt
    import jwt
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️ Install: pip install bcrypt pyjwt")


class AuthSystem:
    """Enterprise-grade authentication system"""
    
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, 'users.json')
        self.sessions_file = os.path.join(data_dir, 'sessions.json')
        self.blocked_file = os.path.join(data_dir, 'blocked.json')
        
        # JWT secret (generate once, store securely)
        self.jwt_secret = os.getenv('JWT_SECRET', self._generate_secret())
        
        # Rate limiting
        self.login_attempts = {}  # IP -> [timestamps]
        self.max_attempts = 5
        self.lockout_duration = 900  # 15 minutes
        
        # Initialize storage
        os.makedirs(data_dir, exist_ok=True)
        self._init_storage()
        
        print("✅ Auth System initialized")
    
    def _generate_secret(self) -> str:
        """Generate secure JWT secret"""
        return secrets.token_urlsafe(32)
    
    def _init_storage(self):
        """Initialize storage files"""
        if not os.path.exists(self.users_file):
            self._save_users({})
        if not os.path.exists(self.sessions_file):
            self._save_sessions({})
        if not os.path.exists(self.blocked_file):
            self._save_blocked({})
    
    def _load_users(self) -> Dict:
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_users(self, users: Dict):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _load_sessions(self) -> Dict:
        """Load sessions from file"""
        try:
            with open(self.sessions_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_sessions(self, sessions: Dict):
        """Save sessions to file"""
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)
    
    def _load_blocked(self) -> Dict:
        """Load blocked IPs/users"""
        try:
            with open(self.blocked_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_blocked(self, blocked: Dict):
        """Save blocked list"""
        with open(self.blocked_file, 'w') as f:
            json.dump(blocked, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password with bcrypt"""
        if CRYPTO_AVAILABLE:
            return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        else:
            # Fallback (NOT SECURE for production)
            return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        if CRYPTO_AVAILABLE:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        else:
            return hashlib.sha256(password.encode()).hexdigest() == hashed
    
    def _check_rate_limit(self, ip: str) -> bool:
        """Check if IP is rate limited"""
        now = time.time()
        
        # Clean old attempts
        if ip in self.login_attempts:
            self.login_attempts[ip] = [
                t for t in self.login_attempts[ip] 
                if now - t < self.lockout_duration
            ]
        
        # Check attempts
        attempts = self.login_attempts.get(ip, [])
        if len(attempts) >= self.max_attempts:
            return False  # Rate limited
        
        return True
    
    def _record_attempt(self, ip: str):
        """Record login attempt"""
        if ip not in self.login_attempts:
            self.login_attempts[ip] = []
        self.login_attempts[ip].append(time.time())
    
    def is_blocked(self, ip: str = None, email: str = None) -> bool:
        """Check if IP or email is blocked"""
        blocked = self._load_blocked()
        
        if ip and ip in blocked.get('ips', []):
            return True
        if email and email in blocked.get('emails', []):
            return True
        
        return False
    
    def block_user(self, ip: str = None, email: str = None, reason: str = ""):
        """Block IP or email"""
        blocked = self._load_blocked()
        
        if 'ips' not in blocked:
            blocked['ips'] = []
        if 'emails' not in blocked:
            blocked['emails'] = []
        
        if ip:
            blocked['ips'].append({
                'ip': ip,
                'reason': reason,
                'blocked_at': datetime.now().isoformat()
            })
        
        if email:
            blocked['emails'].append({
                'email': email,
                'reason': reason,
                'blocked_at': datetime.now().isoformat()
            })
        
        self._save_blocked(blocked)
        print(f"🚫 Blocked: {ip or email} - {reason}")
    
    def create_user(
        self, 
        email: str, 
        password: str, 
        role: str = 'user',
        created_by: str = 'system'
    ) -> Dict:
        """
        Create new user
        
        Roles: admin, user, viewer
        """
        users = self._load_users()
        
        # Check if exists
        if email in users:
            return {'success': False, 'error': 'User already exists'}
        
        # Validate
        if len(password) < 8:
            return {'success': False, 'error': 'Password must be 8+ characters'}
        
        # Create user
        user = {
            'email': email,
            'password_hash': self._hash_password(password),
            'role': role,
            'created_at': datetime.now().isoformat(),
            'created_by': created_by,
            'active': True,
            'last_login': None,
            'login_count': 0
        }
        
        users[email] = user
        self._save_users(users)
        
        print(f"✅ User created: {email} ({role})")
        
        return {
            'success': True,
            'user': {
                'email': email,
                'role': role,
                'created_at': user['created_at']
            }
        }
    
    def login(self, email: str, password: str, ip: str = None) -> Dict:
        """Login user"""
        
        # Check if blocked
        if self.is_blocked(ip=ip, email=email):
            return {
                'success': False,
                'error': 'Access denied',
                'blocked': True
            }
        
        # Check rate limit
        if ip and not self._check_rate_limit(ip):
            return {
                'success': False,
                'error': 'Too many attempts. Try again in 15 minutes.',
                'rate_limited': True
            }
        
        # Record attempt
        if ip:
            self._record_attempt(ip)
        
        # Load users
        users = self._load_users()
        
        # Check user exists
        if email not in users:
            return {'success': False, 'error': 'Invalid credentials'}
        
        user = users[email]
        
        # Check active
        if not user.get('active', True):
            return {'success': False, 'error': 'Account disabled'}
        
        # Verify password
        if not self._verify_password(password, user['password_hash']):
            return {'success': False, 'error': 'Invalid credentials'}
        
        # Update user
        user['last_login'] = datetime.now().isoformat()
        user['login_count'] = user.get('login_count', 0) + 1
        users[email] = user
        self._save_users(users)
        
        # Create session token
        token = self._create_token(email, user['role'])
        
        # Save session
        sessions = self._load_sessions()
        sessions[token] = {
            'email': email,
            'role': user['role'],
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat(),
            'ip': ip
        }
        self._save_sessions(sessions)
        
        print(f"✅ Login successful: {email}")
        
        return {
            'success': True,
            'token': token,
            'user': {
                'email': email,
                'role': user['role']
            }
        }
    
    def _create_token(self, email: str, role: str) -> str:
        """Create JWT token"""
        if CRYPTO_AVAILABLE:
            payload = {
                'email': email,
                'role': role,
                'exp': datetime.utcnow() + timedelta(days=7)
            }
            return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        else:
            # Simple token (NOT SECURE for production)
            return secrets.token_urlsafe(32)
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify token and return user info"""
        sessions = self._load_sessions()
        
        if token not in sessions:
            return None
        
        session = sessions[token]
        
        # Check expiration
        expires_at = datetime.fromisoformat(session['expires_at'])
        if datetime.now() > expires_at:
            del sessions[token]
            self._save_sessions(sessions)
            return None
        
        return {
            'email': session['email'],
            'role': session['role']
        }
    
    def logout(self, token: str):
        """Logout user"""
        sessions = self._load_sessions()
        if token in sessions:
            del sessions[token]
            self._save_sessions(sessions)
            print(f"✅ Logout successful")
    
    def reset_password(self, email: str) -> Dict:
        """Generate password reset token"""
        users = self._load_users()
        
        if email not in users:
            # Don't reveal if user exists
            return {'success': True, 'message': 'If email exists, reset link sent'}
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        
        # Store reset token (expires in 1 hour)
        users[email]['reset_token'] = reset_token
        users[email]['reset_expires'] = (
            datetime.now() + timedelta(hours=1)
        ).isoformat()
        
        self._save_users(users)
        
        print(f"🔑 Reset token for {email}: {reset_token}")
        
        return {
            'success': True,
            'message': 'If email exists, reset link sent',
            'reset_token': reset_token  # In production, send via email
        }
    
    def change_password(self, email: str, new_password: str, reset_token: str = None) -> Dict:
        """Change user password"""
        users = self._load_users()
        
        if email not in users:
            return {'success': False, 'error': 'User not found'}
        
        user = users[email]
        
        # Verify reset token if provided
        if reset_token:
            if user.get('reset_token') != reset_token:
                return {'success': False, 'error': 'Invalid reset token'}
            
            expires = datetime.fromisoformat(user['reset_expires'])
            if datetime.now() > expires:
                return {'success': False, 'error': 'Reset token expired'}
        
        # Validate new password
        if len(new_password) < 8:
            return {'success': False, 'error': 'Password must be 8+ characters'}
        
        # Update password
        user['password_hash'] = self._hash_password(new_password)
        user['reset_token'] = None
        user['reset_expires'] = None
        
        users[email] = user
        self._save_users(users)
        
        print(f"✅ Password changed: {email}")
        
        return {'success': True, 'message': 'Password updated'}
    
    def list_users(self, requester_role: str) -> Dict:
        """List users (admin only)"""
        if requester_role != 'admin':
            return {'success': False, 'error': 'Admin access required'}
        
        users = self._load_users()
        
        user_list = []
        for email, user in users.items():
            user_list.append({
                'email': email,
                'role': user['role'],
                'active': user.get('active', True),
                'created_at': user['created_at'],
                'last_login': user.get('last_login'),
                'login_count': user.get('login_count', 0)
            })
        
        return {
            'success': True,
            'users': user_list,
            'total': len(user_list)
        }
    
    def get_stats(self) -> Dict:
        """Get system stats"""
        users = self._load_users()
        sessions = self._load_sessions()
        blocked = self._load_blocked()
        
        return {
            'total_users': len(users),
            'active_sessions': len(sessions),
            'blocked_ips': len(blocked.get('ips', [])),
            'blocked_emails': len(blocked.get('emails', [])),
            'roles': {
                'admin': len([u for u in users.values() if u['role'] == 'admin']),
                'user': len([u for u in users.values() if u['role'] == 'user']),
                'viewer': len([u for u in users.values() if u['role'] == 'viewer'])
            }
        }


# Initialize auth system
auth = AuthSystem()

# Create initial admin user if none exists
users = auth._load_users()
if not users:
    print("\n🔐 Creating initial admin user...")
    result = auth.create_user(
        email='admin@olympusmont.com',
        password='ChangeMe123!',
        role='admin',
        created_by='system'
    )
    print(f"📧 Email: admin@olympusmont.com")
    print(f"🔑 Password: ChangeMe123!")
    print(f"⚠️  CHANGE PASSWORD IMMEDIATELY\n")


# Test
if __name__ == '__main__':
    print("\n" + "="*60)
    print("AUTH SYSTEM - Test Mode")
    print("="*60 + "\n")
    
    # Test login
    result = auth.login('admin@olympusmont.com', 'ChangeMe123!', ip='127.0.0.1')
    print(json.dumps(result, indent=2))
    
    # Show stats
    print("\n📊 System Stats:")
    print(json.dumps(auth.get_stats(), indent=2))