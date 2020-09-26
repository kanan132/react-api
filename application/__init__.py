import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(Config)



from app import models