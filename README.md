# AES Auth Service

Standalone authentication microservice for AES Logistics.

## Features

- User registration and login
- Role-based access control (driver, pm, admin)
- Session management
- SQLite database
- Flask-based REST API

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_SECRET_KEY="your-secret-key-here"
export ADMIN_EMAIL="admin@example.com"
export ADMIN_PASSWORD="secure-password"

# Run locally
python app.py
```

## API Endpoints

### Authentication

- `POST /api/auth/login` - Login with email and password
- `POST /api/auth/logout` - Logout (clear session)
- `GET /api/auth/me` - Get current user
- `GET /api/auth/health` - Health check

### User Management (Admin only)

- `POST /api/auth/register` - Register new user
- `GET /api/auth/users` - List all users

## Environment Variables

```
FLASK_SECRET_KEY      - Session encryption key (required)
DATABASE_URL          - Path to SQLite database (default: auth.db)
ADMIN_EMAIL           - Admin email for seeding (optional)
ADMIN_PASSWORD        - Admin password for seeding (optional)
PORT                  - Port to run on (default: 5000)
```

## Deployment

### Railway

The service is configured to deploy to Railway. Set these environment variables in Railway:

1. `FLASK_SECRET_KEY` - Generate a random secret key
2. `ADMIN_EMAIL` - Your admin email
3. `ADMIN_PASSWORD` - Your admin password

Railway will automatically:
- Build from the Dockerfile
- Use the `railway.json` configuration
- Deploy on every git push

## Testing

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"secure-password"}'
```

### Get Current User
```bash
curl http://localhost:5000/api/auth/me -b "session=..."
```

### Register User (Admin)
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"pass","role":"driver"}'
```

## Integration with Logistics App

The main logistics app calls this service for authentication:

```python
# Example: logistics app calling auth service
import requests

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://localhost:5000")

def verify_user(email, password):
    resp = requests.post(f"{AUTH_SERVICE_URL}/api/auth/login", json={
        "email": email,
        "password": password
    })
    return resp.json() if resp.status_code == 200 else None
```

## Notes

- Uses SQLite for simplicity; can be upgraded to PostgreSQL for production
- Sessions are stored in Flask's built-in memory; use Redis for multi-instance deployments
- Passwords are hashed with Werkzeug's PBKDF2
