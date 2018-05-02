from flask import Flask
app: Flask = Flask(__name__)
from app import views
