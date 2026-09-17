# Authentication Security Note

## Overview

This project demonstrates defensive authentication controls for a small local Flask web application.

The implementation focuses on safe password storage, server-side validation, secure session handling, rate limiting, generic authentication errors, and automated security testing.

## Security Controls

### 1. Password Hashing

User passwords are never stored in plaintext.

Passwords are hashed using Argon2 before being stored in SQLite.

The database stores a password hash rather than the original password.

### 2. Server-Side Validation

Username and password requirements are validated on the server.

The application rejects invalid usernames and passwords even if client-side validation is bypassed.

### 3. Secure Session Configuration

Authentication sessions use:

* HttpOnly cookies
* SameSite=Lax
* Session expiration
* Session clearing during logout

The session is cleared when authentication succeeds to reduce the risk of session fixation.

For production HTTPS deployment, the Secure cookie flag must be enabled.

### 4. Session Expiration

Authenticated sessions expire after 30 minutes of inactivity according to the configured session lifetime.

### 5. Rate Limiting

Login and registration endpoints are rate limited to:

`5 requests per minute`

This helps reduce automated password-guessing attempts and excessive authentication requests.

### 6. Generic Authentication Errors

The application returns:

`Invalid username or password`

for failed authentication instead of revealing whether a username exists.

This reduces user-enumeration risk.

### 7. SQL Injection Protection

Database queries use parameterized SQL statements.

User-controlled values are passed as parameters rather than concatenated into SQL queries.

### 8. Logout

Logout clears the server-side Flask session data and redirects the user to the login page.

## Testing

Automated tests verify:

* Passwords are hashed
* Successful authentication works
* Incorrect passwords are rejected
* Weak passwords are rejected
* Logout works

Tests can be executed with:

```bash
pytest -v
```

## Production Considerations

This project is intentionally designed as a local educational lab.

A production implementation should additionally consider:

* HTTPS everywhere
* Secure cookie flag
* CSRF protection
* MFA
* Strong secret management
* Account recovery security
* Centralized security logging
* Monitoring and alerting
* Dependency updates
* Database backups
* Reverse-proxy protections
* Stronger abuse detection
* Appropriate privacy controls

No real passwords, API keys, tokens, or personal information should be committed to the repository.
