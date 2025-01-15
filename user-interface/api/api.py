# TO START BACKEND: 
# % . venv/bin/activate
# flask run
from flask import Flask, send_file
app = Flask(__name__)
# import cv2

@app.route('/api/route')
def test():
    return 0

@app.route('/api/photo')
def getPhoto():
    # Path to your image
    photoPath = "testImage.jpg"
    return send_file(photoPath, mimetype='image/jpeg')