# Flask Application Documentation

> Complete documentation for `__init__.py`, `routes.py`, and `security.py`

---

# 1. `__init__.py` — App Initialization

## Overview

This file is the **entry point** for the Flask application. It sets up the core app instance, configures a secret key, and enables CSRF protection globally.

**File Location:** `app/__init__.py`

---

## Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web framework |
| `flask_wtf.csrf` | CSRF protection extension |

---

## Code Breakdown

```python
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = "super_secret_key"
csrf = CSRFProtect(app)
```

### `app = Flask(__name__)`
Creates the Flask application instance. `__name__` tells Flask the root path of the application.

### `app.secret_key`
Used by Flask to sign session cookies and other security-sensitive data.

> ⚠️ **Warning:** The current value `"super_secret_key"` is a placeholder. In production, replace it with a strong, randomly generated key stored in an environment variable.

```python
# Recommended production approach
import os
app.secret_key = os.environ.get("SECRET_KEY")
```

### `csrf = CSRFProtect(app)`
Enables **Cross-Site Request Forgery (CSRF)** protection across all forms in the application. This prevents malicious sites from making unauthorized requests on behalf of authenticated users.

---

## Security Notes

- Never hardcode secret keys in source code.
- Use `.env` files or secret managers (e.g., AWS Secrets Manager, HashiCorp Vault) in production.
- CSRF protection is enabled globally — no need to add it per-route.

---

# 2. `routes.py` — Application Routes

## Overview

This file defines the **URL routes** for the Flask application. It currently contains one route that allows a logged-in user to securely fetch their own ballot data.

**File Location:** `routes.py`

---

## Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web framework (Flask, request, jsonify, session) |
| `models` | Database models (Ballot) |

---

## Routes

### `GET /ballot/<ballot_id>`

Fetches the ballot belonging to the currently logged-in user.

```python
@app.route("/ballot/<int:ballot_id>")
def get_ballot(ballot_id):
    user_id = session.get("user_id")
    ballot = Ballot.query.filter_by(id=ballot_id, user_id=user_id).first()
    if not ballot:
        return jsonify({"error": "Unauthorized access"}), 403
    return jsonify({"vote": ballot.vote})
```

#### Parameters

| Parameter | Type | Location | Description |
|---|---|---|---|
| `ballot_id` | `int` | URL path | The ID of the ballot to retrieve |

#### Session

| Key | Description |
|---|---|
| `user_id` | ID of the currently authenticated user, read from the session |

#### Responses

| Status Code | Condition | Response Body |
|---|---|---|
| `200 OK` | Ballot found and belongs to user | `{ "vote": <vote_value> }` |
| `403 Forbidden` | Ballot not found or does not belong to user | `{ "error": "Unauthorized access" }` |

---

## Security Notes

- **Authorization check:** The query filters by both `ballot_id` **and** `user_id` from the session. This prevents users from accessing other users' ballots (Insecure Direct Object Reference / IDOR protection).
- The session `user_id` must be set during login — ensure the login route properly authenticates users before writing to the session.
- If `user_id` is not in the session (unauthenticated user), `session.get("user_id")` returns `None`, and the query will return no results, triggering the 403 response.

---

## Example Request

```http
GET /ballot/42
Cookie: session=<valid_session_cookie>
```

### Success Response

```json
{
  "vote": "Candidate A"
}
```

### Error Response

```json
{
  "error": "Unauthorized access"
}
```

---

# 3. `security.py` — Security Headers

## Overview

This file adds **HTTP security response headers** to every outgoing response from the Flask application. It uses Flask's `after_request` hook to automatically inject these headers without modifying individual route handlers.

**File Location:** `app/security.py`

---

## Code Breakdown

```python
@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'none'"
    return response
```

### `@app.after_request`
A Flask decorator that registers a function to run **after every request**, just before the response is sent to the client. The function receives the response object and must return it (modified or unmodified).

---

## Headers Applied

### `X-Frame-Options: DENY`

| Detail | Value |
|---|---|
| Header | `X-Frame-Options` |
| Value | `DENY` |
| Purpose | Prevents the page from being embedded inside a `<frame>`, `<iframe>`, or `<object>` |

**Protects against:** Clickjacking attacks, where an attacker embeds your page inside an invisible frame to trick users into clicking UI elements unknowingly.

> `DENY` means the page cannot be framed by **any** origin, including the same site.

---

### `Content-Security-Policy: frame-ancestors 'none'`

| Detail | Value |
|---|---|
| Header | `Content-Security-Policy` |
| Directive | `frame-ancestors 'none'` |
| Purpose | Modern replacement for `X-Frame-Options`, supported by all current browsers |

**Protects against:** Same clickjacking threat as above, but provides more granular control and is part of the broader Content Security Policy standard.

> Both headers are set together for **maximum browser compatibility** — older browsers respect `X-Frame-Options`, while modern browsers prioritize `Content-Security-Policy`.

---

## Security Notes

- This function is applied **globally** — every response from the app will include these headers.
- Consider extending this function with additional security headers for defense-in-depth:

```python
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
```

- Ensure this file is **imported** in `__init__.py` or the application factory so the `after_request` hook is registered.

---

## Related Resources

- [OWASP Clickjacking Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html)
- [MDN: X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)
- [MDN: Content-Security-Policy frame-ancestors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors)