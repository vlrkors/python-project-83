from __future__ import annotations

import os
from flask import Flask
from dotenv import load_dotenv


load_dotenv(override=False)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.get("/")
def index():
    return {"message": "Hello, Hexlet!"}
