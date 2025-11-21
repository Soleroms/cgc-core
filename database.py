"""
Database Layer - PostgreSQL + JSON fallback
"""

import os
import json
from typing import Dict, Optional, List
from datetime import datetime, timezone

# Try PostgreSQL
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


class Database:
    """Unified database interface with PostgreSQL and JSON file fallback."""
    
    def __init__(self):
        self.postgres_url = os.getenv('DATABASE_URL')
        self.use_postgres = False
        
        if self.postgres_url and POSTGRES_AVAILABLE:
            try:
                # Attempt PostgreSQL connection
                self.conn = psycopg2.connect(self.postgres_url)
                self.use_postgres = True
                self._create_tables()
                print("[DB] Database: PostgreSQL active")
            except Exception as e:
                # Fallback to JSON if PG is configured but connection fails
                print(f"[DB] Database: JSON files fallback (PG connection failed: {e})")
                self._setup_json_fallback()
        else:
            # Fallback to JSON if PG is not configured or psycopg2 is not installed
            self._setup_json_fallback()
            print("[DB] Database: JSON files fallback")

    def _setup_json_fallback(self):
        """Initializes settings and files for JSON fallback mode."""
        self.use_postgres = False
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
        self._init_json()
        
    def _create_tables(self):
        """Create PostgreSQL tables (users, tenants, sessions)."""
        with self.conn.cursor() as cur:
            # Table 1: users
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    email VARCHAR(255) PRIMARY KEY,
                    password_hash VARCHAR(255) NOT NULL,
                    name VARCHAR(255),
                    role VARCHAR(50) DEFAULT 'user',
                    tenant_id VARCHAR(255) REFERENCES tenants(tenant_id),
                    created_at TIMESTAMP WITH TIME ZONE,
                    last_login TIMESTAMP WITH TIME ZONE
                )
            """)
            # Table 2: tenants
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tenants (
                    tenant_id VARCHAR(255) PRIMARY KEY,
                    org_name VARCHAR(255) NOT NULL,
                    plan VARCHAR(50) DEFAULT 'basic',
                    api_key VARCHAR(255),
                    status VARCHAR(50) DEFAULT 'active',
                    created_at TIMESTAMP WITH TIME ZONE
                )
            """)
            # Table 3: sessions
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    token VARCHAR(255) PRIMARY KEY,
                    email VARCHAR(255) NOT NULL REFERENCES users(email),
                    created_at TIMESTAMP WITH TIME ZONE,
                    expires_at TIMESTAMP WITH TIME ZONE
                )
            """)
            self.conn.commit()
    
    def _init_json(self):
        """Initialize JSON files for users, sessions, and tenants (FIXED: added tenants)."""
        self.users_file = os.path.join(self.data_dir, 'users.json')
        self.sessions_file = os.path.join(self.data_dir, 'sessions.json')
        self.tenants_file = os.path.join(self.data_dir, 'tenants.json') # <-- ADDED
        
        for file in [self.users_file, self.sessions_file, self.tenants_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f)

    def _read_json(self, file_path: str) -> Dict:
        """Helper to read data from a JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def _write_json(self, file_path: str, data: Dict):
        """Helper to write data to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    # --- USER METHODS ---
    
    def get_user(self, email: str) -> Optional[Dict]:
        """Retrieve user by email."""
        if self.use_postgres:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                row = cur.fetchone()
                return dict(row) if row else None
        else:
            return self._read_json(self.users_file).get(email)
    
    def save_user(self, email: str, data: Dict):
        """Create or update user. Expects 'password_hash' and 'created_at' for new users."""
        if self.use_postgres:
            # FIX: Ensure all required fields for INSERT are present.
            # Use data.get() for optional fields.
            current_time = datetime.now(timezone.utc)

            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (email, password_hash, name, role, tenant_id, created_at, last_login)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (email) DO UPDATE SET
                    password_hash = EXCLUDED.password_hash,
                    name = EXCLUDED.name,
                    role = EXCLUDED.role,
                    tenant_id = EXCLUDED.tenant_id,
                    last_login = %s  -- Explicitly update last_login
                """, (email, data['password_hash'], data.get('name', ''), 
                      data.get('role', 'user'), data.get('tenant_id'), 
                      data.get('created_at', current_time), data.get('last_login', current_time), current_time))
                self.conn.commit()
        else:
            users = self._read_json(self.users_file)
            users[email] = data
            self._write_json(self.users_file, users)

    def update_user_login(self, email: str):
        """Updates the last_login timestamp for a user."""
        current_time = datetime.now(timezone.utc)
        if self.use_postgres:
            with self.conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET last_login = %s WHERE email = %s", 
                    (current_time, email)
                )
                self.conn.commit()
        else:
            # JSON implementation requires reading and rewriting the whole user dict
            users = self._read_json(self.users_file)
            if email in users:
                users[email]['last_login'] = current_time.isoformat()
                self._write_json(self.users_file, users)

    # --- SESSION METHODS (ADDED for consistency) ---

    def get_session(self, token: str) -> Optional[Dict]:
        """Retrieve session by token."""
        if self.use_postgres:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM sessions WHERE token = %s AND expires_at > NOW()", (token,))
                row = cur.fetchone()
                return dict(row) if row else None
        else:
            sessions = self._read_json(self.sessions_file)
            session_data = sessions.get(token)
            if session_data:
                # Basic check for expiry in JSON mode
                if session_data.get('expires_at') and session_data['expires_at'] > datetime.now(timezone.utc).isoformat():
                    return session_data
            return None
    
    def save_session(self, token: str, data: Dict):
        """Create or update session."""
        if self.use_postgres:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO sessions (token, email, created_at, expires_at)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (token) DO UPDATE SET
                    expires_at = EXCLUDED.expires_at
                """, (token, data['email'], data.get('created_at'), data.get('expires_at')))
                self.conn.commit()
        else:
            sessions = self._read_json(self.sessions_file)
            sessions[token] = data
            self._write_json(self.sessions_file, sessions)

    def delete_session(self, token: str):
        """Delete session by token."""
        if self.use_postgres:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM sessions WHERE token = %s", (token,))
                self.conn.commit()
        else:
            sessions = self._read_json(self.sessions_file)
            if token in sessions:
                del sessions[token]
                self._write_json(self.sessions_file, sessions)

    # --- TENANT METHODS (ADDED for consistency) ---
    
    def get_tenant(self, tenant_id: str) -> Optional[Dict]:
        """Retrieve tenant by ID."""
        if self.use_postgres:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM tenants WHERE tenant_id = %s", (tenant_id,))
                row = cur.fetchone()
                return dict(row) if row else None
        else:
            return self._read_json(self.tenants_file).get(tenant_id)
            
    def save_tenant(self, tenant_id: str, data: Dict):
        """Create or update tenant."""
        if self.use_postgres:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO tenants (tenant_id, org_name, plan, api_key, status, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (tenant_id) DO UPDATE SET
                    org_name = EXCLUDED.org_name,
                    plan = EXCLUDED.plan,
                    api_key = EXCLUDED.api_key,
                    status = EXCLUDED.status
                """, (tenant_id, data['org_name'], data.get('plan'), 
                      data.get('api_key'), data.get('status'), data.get('created_at')))
                self.conn.commit()
        else:
            tenants = self._read_json(self.tenants_file)
            tenants[tenant_id] = data
            self._write_json(self.tenants_file, tenants)

# --- SINGLETON PATTERN ---

_db: Optional['Database'] = None

def get_database():
    """Initializes and returns the singleton Database instance."""
    global _db
    if _db is None:
        _db = Database()
    return _db