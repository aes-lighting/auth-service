#!/usr/bin/env python3
"""
AES Auth Service - Standalone Authentication Microservice

Handles all user authentication for AES Logistics:
- User registration
- Login/logout
- Session management
- Role-based access

API Endpoints:
  POST   /api/auth/login          - Login (email + password)
  POST   /api/auth/logout         - Logout (clear session)
  GET    /api/auth/me             - Get current user
  POST   /api/auth/register       - Admin: Register new user
  GET    /api/auth/users          - Admin: List all users
  GET    /api/auth/verify         - Verify auth token

Environment Variables:
  FLASK_SECRET_KEY                - Session encryption key (required)
  DATABASE_URL                    - SQLite database path (default: auth.db)
  ADMIN_EMAIL                     - Initial admin email (seeded on startup)
  ADMIN_PASSWORD                  - Initial admin password (seeded on startup)
  PORT                            - Port to run on (default: 5000)
"""

import json
import logging
import os
import secrets
from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# ===== Configuration =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.environ.get("DATABASE_URL", os.path.join(BASE_DIR, "auth.db"))
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@aes-energy.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "aes")
PORT = int(os.environ.get("PORT", 5000))

if not FLASK_SECRET_KEY:
    FLASK_SECRET_KEY = secrets.token_hex(32)
    print(
        f"⚠️  WARNING: FLASK_SECRET_KEY not set. Using random key: {FLASK_SECRET_KEY}",
        flush=True
    )

# ===== Flask Setup =====
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  # Only send over HTTPS in production
    PERMANENT_SESSION_LIFETIME=60 * 60 * 24 * 30,  # 30 days
)

# ===== CORS Setup =====
CORS(app, supports_credentials=True)

# ===== Logging =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
log = logging.getLogger("aes_auth")

# ===== Database Initialization =====
def init_db():
    """Initialize SQLite database with users table."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'driver',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    log.info(f"Database initialized at {DATABASE_URL}")

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def seed_admin():
    """Seed/recreate admin user with ADMIN_EMAIL and ADMIN_PASSWORD."""
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        log.info("No ADMIN_EMAIL/ADMIN_PASSWORD set; skipping admin seeding.")
        return

    conn = get_db()
    cursor = conn.cursor()

    try:
        # Delete any existing admin user with this email to ensure fresh credentials
        cursor.execute("DELETE FROM users WHERE email = ?", (ADMIN_EMAIL,))

        password_hash = generate_password_hash(ADMIN_PASSWORD)
        now = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO users (email, name, password_hash, role, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ADMIN_EMAIL, "Admin", password_hash, "admin", now, now))

        conn.commit()
        log.info(f"Seeded/refreshed admin user: {ADMIN_EMAIL}")
    except Exception as e:
        log.error(f"Error seeding admin: {e}")
    finally:
        conn.close()

# ===== Auth Decorators =====
def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Not authenticated"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Not authenticated"}), 401

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (session["user_id"],))
        row = cursor.fetchone()
        conn.close()

        if not row or row["role"] != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return f(*args, **kwargs)
    return decorated_function

# ===== Auth Routes =====

@app.route("/api/auth/login", methods=["POST"])
def login():
    """Login with email and password."""
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, name, role, password_hash FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if not row or not check_password_hash(row["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Set session
    session["user_id"] = row["id"]
    session.permanent = True

    log.info(f"User logged in: {email} ({row['role']})")

    return jsonify({
        "user_id": row["id"],
        "email": row["email"],
        "name": row["name"],
        "role": row["role"]
    }), 200

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logout (clear session)."""
    email = session.get("email", "unknown")
    session.clear()
    log.info(f"User logged out: {email}")
    return jsonify({"message": "Logged out"}), 200

@app.route("/api/auth/me", methods=["GET"])
@login_required
def get_current_user():
    """Get current authenticated user."""
    user_id = session.get("user_id")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, name, role FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": row["id"],
        "email": row["email"],
        "name": row["name"],
        "role": row["role"]
    }), 200

@app.route("/api/auth/register", methods=["POST"])
@admin_required
def register_user():
    """Register a new user (admin only)."""
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = (data.get("role") or "driver").strip().lower()

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password required"}), 400

    if role not in ("driver", "pm", "admin"):
        return jsonify({"error": "Invalid role. Must be: driver, pm, admin"}), 400

    password_hash = generate_password_hash(password)
    now = datetime.now().isoformat()

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (email, name, password_hash, role, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email, name, password_hash, role, now, now))
        conn.commit()
        user_id = cursor.lastrowid

        log.info(f"User registered: {email} ({role})")

        return jsonify({
            "user_id": user_id,
            "email": email,
            "name": name,
            "role": role,
            "message": "User registered successfully"
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409
    finally:
        conn.close()

@app.route("/api/auth/users", methods=["GET"])
@admin_required
def list_users():
    """List all users (admin only)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, name, role, created_at FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    users = [
        {
            "user_id": row["id"],
            "email": row["email"],
            "name": row["name"],
            "role": row["role"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]

    return jsonify({"users": users}), 200
@app.route("/api/auth/admin/register_user", methods=["POST"])
def admin_register_user_header():
    """Register a new user (header-based auth for microservices)."""
    try:
        # Check Authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization required"}), 401
        
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or os.environ.get("SHARED_PASSWORD", "aes")
        role = (data.get("role") or "driver").strip().lower()

        if not name or not email:
            return jsonify({"error": "Name and email required"}), 400

        if role not in ("driver", "pm", "admin"):
            return jsonify({"error": "Invalid role. Must be: driver, pm, admin"}), 400

        password_hash = generate_password_hash(password)
        now = datetime.now().isoformat()

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (email, name, password_hash, role, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email, name, password_hash, role, now, now))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        log.info(f"User registered: {email} ({role})")

        return jsonify({
            "user_id": user_id,
            "email": email,
            "name": name,
            "role": role
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409
    except Exception as e:
        log.error(f"Error registering user: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/auth/admin/users", methods=["GET"])
def admin_list_users_header():
    """List all users (header-based auth for microservices)."""
    try:
        # Check Authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization required"}), 401
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, name, role, created_at FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()

        users = [
            {
                "user_id": row["id"],
                "email": row["email"],
                "name": row["name"],
                "role": row["role"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]

        return jsonify({"users": users}), 200
    except Exception as e:
        log.error(f"Error listing users: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/api/auth/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

# ===== Initialize on App Creation =====
@app.before_request
def before_first_request():
    """Initialize database on first request."""
    if not hasattr(app, 'initialized'):
        log.info("Starting AES Auth Service...")
        init_db()
        seed_admin()
        log.info(f"Listening on port {PORT}")
        app.initialized = True

# ===== Main =====
if __name__ == "__main__":
    log.info("Starting AES Auth Service...")
    init_db()
    seed_admin()
    log.info(f"Listening on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
