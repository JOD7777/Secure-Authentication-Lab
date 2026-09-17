# 🔐 Secure Authentication Lab

A beginner-friendly local authentication service built with Python and Flask to demonstrate defensive authentication security controls.

## 🎯 Objective

Implement and test:

* Secure password hashing
* Server-side validation
* Secure session cookies
* Session expiration
* Logout
* Rate limiting
* Generic authentication errors
* Automated security tests

## 🛠️ Technologies

* Python
* Flask
* SQLite
* Argon2
* Flask-Limiter
* Pytest

## 📁 Project Structure

```text
secure-auth-lab/
├── app.py
├── requirements.txt
├── README.md
├── SECURITY.md
├── .gitignore
├── templates/
│   └── login.html
└── tests/
    └── test_auth.py
```

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd secure-auth-lab
```

Create a virtual environment:

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux/Kali

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

```bash
python app.py
```

The application runs locally at:

```text
http://127.0.0.1:5000
```

## 🧪 Run Security Tests

```bash
pytest -v
```

The tests verify password hashing, authentication, invalid password handling, validation, and logout.

## 🔒 Security Controls

| Control                  | Implementation        |
| ------------------------ | --------------------- |
| Password hashing         | Argon2                |
| Input validation         | Server-side           |
| SQL injection protection | Parameterized queries |
| Session protection       | HttpOnly + SameSite   |
| Session expiration       | 30 minutes            |
| Login rate limiting      | 5/minute              |
| Generic login errors     | Enabled               |
| Logout                   | Session cleared       |
| Automated tests          | Pytest                |

## ⚠️ Educational Use

This project is intended for a local cybersecurity learning environment.

Do not use the default development configuration directly for a production application.

Never commit:

* Passwords
* API keys
* Session secrets
* `.env` files
* User databases
* Personal information

## 📜 License

MIT License

## 👤 Author

Supriyo Malik

Cybersecurity & Advanced Networking Student
