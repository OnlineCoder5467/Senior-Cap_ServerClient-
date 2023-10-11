import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import json
import random

load_dotenv()

UPLOAD_FOLDER = '../imagebucket/'
UNVERIFIED_BUCKET = '../imagebucket'

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "Hello, World! You may need to log in, I'll direct you"


@app.get('/upload')
def upload_get():
    return '''
      <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
      </form>
        '''


@app.route("/upload", methods=["POST"])
def upload_file():
  file = request.files["file"]
  file.save(os.path.join(UPLOAD_FOLDER, file.filename))
  return "do not test this page"


@app.route("/checkModelVersion")
def checkModelVersion():
  return "Current model version#_____"


@app.route("/downloadModel")
def downloadModel():
  return "Downloading model #_____"

#returns sample json of newly uploaded objects for admin review
@app.route("/getUniverifiedXs")
def getUnverifiedXs():
    images = []
    imageID = 0
    
    for image in os.listdir(UNVERIFIED_BUCKET):
        atag = getTag()
        images.append({
            "id": imageID,
            "imageUrl": f"http://localhost:5000/imagebucket/{image}",
            "tag": atag
        })
        imageID += 1

    response_data = {
        "imageCount": len(images),
        "images": images
    }        
    return jsonify(response_data)

def getTag():
  if (random.randint(1, 2) == 1):
     return "dog"
  return "cat"
   

#returns sample json of newly uploaded objects for admin review
@app.route("/getUniverifiedYs")
def getUnverifiedYs():
    images = []
    imageID = 0
    
    for image in os.listdir(UNVERIFIED_BUCKET):
        atag = getTag()
        images.append({
            "id": imageID,
            "imageUrl": f"http://localhost:5000/imagebucket/{image}",
            "tag": atag
        })
        imageID += 1
    return jsonify(images)


@app.route("/updateUnverified")
def updateUnverified():
   return "Success"

   

if __name__ == "__main__":
  app.run()