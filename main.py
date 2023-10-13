import os
from flask import Flask, request, jsonify, url_for
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import json
import random
from flask_cors import CORS
import requests

load_dotenv()

UPLOAD_FOLDER = './imagebucket/'
UNVERIFIED_BUCKET = './imagebucket'
API_ENDPOINT = 'https://mt5t6im18f.execute-api.us-west-1.amazonaws.com/dev'

app = Flask(__name__)
CORS(app)

data = []


def getInitialData():
  response = requests.get(API_ENDPOINT)
  if response.status_code != 200:
    return jsonify({"error": "Failed to retrieve images"}), 500
  api_images = response.json()
  data.clear()
  for i in api_images:
    data.append(i)
  print(data)
  return


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
  S3_BUCKET_URL = f"https://seniorcapstone.s3.amazonaws.com/{file.filename}"
  headers = {'Content-Type': file.content_type}
  response = requests.put(S3_BUCKET_URL, headers=headers, data=file)
  if response.status_code == 200:
    getInitialData()
    return "File uploaded successfully!"
  else:
    return f"Failed to upload: {response.text}"


@app.route("/checkModelVersion")
def checkModelVersion():
  return "Current model version#_____"


@app.route("/downloadModel")
def downloadModel():
  return "Downloading model #_____"


def getTag():
  if (random.randint(1, 2) == 1):
    return "dog"
  return "cat"


@app.route("/getUnverifiedXs")
def getUnverifiedXs():
  resonseObject = []
  imageID = 0
  for d in data:
    atag = getTag()
    confidence = 90 if atag in d else 10
    resonseObject.append({
        "id": imageID,
        "imageUrl": d,
        "tag": atag,
        "confidence": confidence
    })
    imageID += 1
  return jsonify(resonseObject)


@app.route("/getUniverifiedYs")
def getUnverifiedYs():
  images = []
  imageID = 0
  for image in os.listdir(UNVERIFIED_BUCKET):
    atag = getTag()
    images.append({
        "id": imageID,
        "imageUrl":
        f"https://replit.com/@jondooley87/flaskapp#imagebucket/{image}",
        "tag": atag
    })
    imageID += 1
  return jsonify(images)


@app.route("/updateUnverified")
def updateUnverified():
  return "Success"


@app.route("/signupAdmin")
def signupAdmin():
  return "Hey New Admin"


@app.route("/signinAdmin")
def signinAdmin():
  return "Admin signed in"


@app.route("/signoutAdmin")
def signoutAdmin():
  return "Signed out Admin"


@app.route("/trainModel")
def trainModel():
  return "Training"


@app.route("/updateAndArchiveModel")
def updateAndArchiveModel():
  return "New Model Up"


if __name__ == '__main__':
  getInitialData()
  app.run(host='0.0.0.0', port=81)
'''THIS FUNCTION RETURNS A JSON WITH IMAGE COUNT AND ALL IMAGES FROM LOCAL FOLDER
#returns sample json of newly uploaded objects for admin review
@app.route("/getUnverifiedXs")
def getUnverifiedXs():
  images = []
  imageID = 0
  for image in os.listdir(UNVERIFIED_BUCKET):
    atag = getTag()
    images.append({
        "id": imageID,
        "imageUrl": url_for("imagebucket", filename=image),
        "tag": atag
    })
    imageID += 1
  response_data = {"imageCount": len(images), "images": images}
  return jsonify(response_data)
'''
'''THIS FUNCTION RETRIEVES JSON OF IMAGES ONLY FROM LOCAL FOLDER
@app.route("/getUnverifiedXs")
def getUnverifiedXs():
  response = requests.get(API_ENDPOINT)
  if response.status_code != 200:
    return jsonify({"error": "Failed to retrieve images"}), 500
  api_images = response.json()
  images = []
  imageID = 0  # Start from 0    
  for imageUrl in api_images:
    atag = getTag()
    images.append({"id": imageID, "imageUrl": imageUrl, "tag": atag})
    imageID += 1  # Increment the imageID for the next iteration
  return jsonify(images)
'''
'''#THIS FUNCTION SAVES SINGLE IMAGE TO LOCAL FOLDER
@app.route("/upload", methods=["POST"])
def upload_file():
  file = request.files["file"]
  #  file.save(os.path.join(UPLOAD_FOLDER, file.filename))
  res = requests.post(
      #  'https://example.com/api/users',
      'https://s3.amazonaws.com/seniorcapstone/{file.filename}'
      #except Exception as e:
      #  return "Did not work, try again later"
  )
  return "It worked"
'''
