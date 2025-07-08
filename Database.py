import sqlite3
import json
from Context import UserSessionContext
from datetime import datetime
import os

DB_PATH = "user_sessions.db"

# Ensure table exists
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        # Check if sessions table exists and has the new columns
        try:
            conn.execute("SELECT name, email, created_at, last_updated FROM sessions LIMIT 1")
        except sqlite3.OperationalError:
            # Table exists but doesn't have new columns, recreate it
            conn.execute("DROP TABLE IF EXISTS sessions")
            conn.execute("""
                CREATE TABLE sessions (
                    uid INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    data TEXT NOT NULL,
                    created_at TEXT,
                    last_updated TEXT
                )
            """)
        else:
            # Table exists with new columns, create if not exists
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    uid INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    data TEXT NOT NULL,
                    created_at TEXT,
                    last_updated TEXT
                )
            """)
        
        # Create users table for registration
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT,
                created_at TEXT,
                last_login TEXT
            )
        """)

def create_user(name: str, email: str = None, password_hash: str = None) -> int:
    """Create a new user and return their UID."""
    try:
        with sqlite3.connect(DB_PATH, timeout=30.0) as conn:
            # Enable WAL mode to prevent database locking
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA busy_timeout=30000")
            
            now = datetime.now().isoformat()
            
            # Check if user already exists
            if email:
                existing = conn.execute("SELECT uid FROM users WHERE email = ?", (email,)).fetchone()
                if existing:
                    raise ValueError(f"User with email {email} already exists")
            
            cursor = conn.execute(
                "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (name, email, password_hash, now)
            )
            uid = cursor.lastrowid
            
            # Create initial session context
            context = UserSessionContext(
                name=name,
                uid=uid,
                email=email,
                created_at=now,
                last_updated=now
            )
            
            # Save session context in the same transaction
            context.last_updated = now
            data = context.model_dump_json()
            conn.execute("""
                INSERT OR REPLACE INTO sessions (uid, name, email, data, created_at, last_updated) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (uid, name, email, data, now, now))
            
            conn.commit()
            return uid
            
    except Exception as e:
        print(f"Database error: {e}")
        raise

def get_user_by_email(email: str) -> dict | None:
    """Get user by email."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cur.fetchone()
        if row:
            return {
                "uid": row[0],
                "name": row[1],
                "email": row[2],
                "password_hash": row[3],
                "created_at": row[4],
                "last_login": row[5]
            }
        return None

def get_user_by_uid(uid: int) -> dict | None:
    """Get user by UID."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT * FROM users WHERE uid = ?", (uid,))
        row = cur.fetchone()
        if row:
            return {
                "uid": row[0],
                "name": row[1],
                "email": row[2],
                "password_hash": row[3],
                "created_at": row[4],
                "last_login": row[5]
            }
        return None

def update_last_login(uid: int):
    """Update user's last login time."""
    with sqlite3.connect(DB_PATH) as conn:
        now = datetime.now().isoformat()
        conn.execute("UPDATE users SET last_login = ? WHERE uid = ?", (now, uid))
        conn.commit()

def save_session(context: UserSessionContext):
    """Save user session context."""
    with sqlite3.connect(DB_PATH) as conn:
        context.last_updated = datetime.now().isoformat()
        data = context.model_dump_json()
        conn.execute("""
            INSERT OR REPLACE INTO sessions (uid, name, email, data, created_at, last_updated) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (context.uid, context.name, context.email, data, context.created_at, context.last_updated))
        conn.commit()

def load_session(uid: int) -> UserSessionContext | None:
    """Load user session context."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT data FROM sessions WHERE uid = ?", (uid,))
        row = cur.fetchone()
        if row:
            return UserSessionContext.model_validate_json(row[0])
        return None

def get_all_users() -> list:
    """Get all registered users."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT uid, name, email, created_at, last_login FROM users")
        return [{"uid": row[0], "name": row[1], "email": row[2], "created_at": row[3], "last_login": row[4]} for row in cur.fetchall()] 