from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv(override=False)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.get("/")
def index():
    return render_template("index.html")
