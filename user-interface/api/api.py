# TO START BACKEND: 
# % . venv/bin/activate
# flask run

from flask import Flask, send_file

app = Flask(__name__)
import json
# import cv2

@app.route('/getData')
def getData():

    file_path = "data.json"

    # Open and read the JSON file
    with open(file_path, "r") as file:
        data = json.load(file)
    
    return data
    

# @app.route('/api/photo')
# def getPhoto():
#     # Path to your image
#     photoPath = "testImage.jpg"
#     return send_file(photoPath, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(debug=True)

