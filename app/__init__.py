# app/__init__.py
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = "super_secret_key"  # replace with a secure key in production
csrf = CSRFProtect(app)
