from werkzeug.security import generate_password_hash

users = {
    "admin": "admin123",
    "dr_ravi": "doctor123",
    "reception1": "reception123",
    "account1": "account123"
}

for username, password in users.items():
    print(f"{username}:")
    print(generate_password_hash(password))
    print()