from flask import render_template, request, jsonify
from app import app
import os

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/videos")
def list_videos():
    videos = os.listdir("recordings")
    return render_template("videos.html", videos=videos)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        # Mettre à jour les paramètres
        data = request.json
        # Exemple de mise à jour des paramètres dans un fichier config
        return jsonify({"status": "success"})
    return render_template("settings.html")
