from flask import Flask
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World! Ceci est ma page principale."

print("NumPy version:", np.__version__)
print("OpenCV version:", cv2.__version__)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
