import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import json
import random
from flask_cors import CORS
import requests
import time
import logging

load_dotenv()

#UPLOAD_FOLDER = './imagebucket/'
UNVERIFIED_BUCKET = './unverifiedbucket/'
API_ENDPOINT = 'https://mt5t6im18f.execute-api.us-west-1.amazonaws.com/dev'
S3_BUCKET = "https://seniorcapstone.s3.amazonaws.com/"
OTHER_BUCKET = './otherbucket/'
unverifiedObjectsJSON = './otherbucket/unverifiedObjects.json'
verifiedObjectsJSON = './otherbucket/verifiedObjects.json'
labelsJSON = './otherbucket/labels.json'

#app = Flask(__name__)
app = Flask(__name__, static_folder=UNVERIFIED_BUCKET)

CORS(app)

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)


data = []
unverified_data = []
Labels = []

@app.route("/")
def hello_world():
      # app.logger.debug("This will show debug messages and above")
      # app.logger.info("This will show info messages and above")
      # app.logger.warning("This will show warning messages and above")
      # app.logger.error("This will show error messages and above")
      # app.logger.critical("This will show critical messages")
  getInitialData()    
  return x


@app.route("/getUnverifiedXs")
def getUnverifiedXs():
  images = []
  imageCount = 0
  datalabels = []
  for data in unverified_data:
    images.append({
        "id": data.get("id"),
        "imageUrl": '/images/' + data.get("id"),
        "Label": data.get("Label"),
        "confidence": data.get("confidence"),
    })
    datalabels.append(data.get("Label"))
    imageCount += 1
  response_data = {"imageCount": len(images), "labels": datalabels,  "images": images}
  return jsonify(response_data)




@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.static_folder, filename)

def getInitialData():
##set Labels coll
  try:
    if os.path.isfile(labelsJSON) and os.path.getsize(labelsJSON) > 0:
      with open(labelsJSON, 'r') as json_file:
        Labels.clear()
        Labels.extend(json.load(json_file))
  except Exception as e:
    app.logger.error(f"An error occurred: {e}")
    return "oh no i messed up"
##set unverified_data
  try:
    if os.path.isfile(unverifiedObjectsJSON) and os.path.getsize(unverifiedObjectsJSON) > 0:
      with open(unverifiedObjectsJSON, 'r') as json_file:
        unverifiedObjects = json.load(json_file)
        unverified_data.clear()
        unverified_data.extend(unverifiedObjects)
    else:
      app.logger.warning(f"File {unverifiedObjectsJSON} does not exist or is empty.")
  except json.JSONDecodeError as e:
   app.logger.error(f"JSON decode error: {e}")
  except Exception as e:
    app.logger.error(f"An error occurred: {e}")
  return unverified_data

def getTimeTxt():
  timestamp = time.time()
  timestamp_str = str(timestamp)
  last_five_digits = timestamp_str[-5:]
  return last_five_digits


@app.get('/seeUnverified')
def seeUnverified():
  return jsonify(unverified_data)

@app.route('/uploadV2', methods=["GET", "POST"])
def uploadV2():
  if request.method == "GET":
    return '''
        <form action="/uploadV2" method="post" enctype="multipart/form-data">
            <label for="file">Choose file:</label>
            <input type="file" name="file" required><br><br>

            <label for="Label">Label:</label>
            <input type="text" name="Label" required><br><br>

            <label for="confidence">Confidence:</label>
            <input type="number" name="confidence" required><br><br>

            <input type="submit" value="Upload">
        </form>
      '''
  elif request.method == "POST":
    currTime = getTimeTxt()
    file = request.files["file"]
    original_filename = secure_filename(file.filename)
    file_name, file_extension = os.path.splitext(original_filename)
    filename = f"{file_name}{currTime}{file_extension}"
    filepath = os.path.join(UNVERIFIED_BUCKET, filename)
  #  s3path = f"{S3_BUCKET}{filename}"
    try:
      file.save(filepath)
      newUnverified = {
        "id": filename,
        "imageUrl": f"/images/{filename}",
        "Label": request.form["Label"],
        "confidence": request.form["confidence"]
      }
      if newUnverified.get("Label") not in Labels:
        addLabelHandler(newUnverified.get("Label"))
      if os.path.isfile(unverifiedObjectsJSON) and os.path.getsize(unverifiedObjectsJSON) > 0:
          with open(unverifiedObjectsJSON, "r") as f:
              unverifiedObjects = json.load(f)
      else:
          unverifiedObjects = []
      unverifiedObjects.append(newUnverified)
      with open(unverifiedObjectsJSON, "w") as f:
          json.dump(unverifiedObjects, f)
      unverified_data.append(newUnverified)
    except Exception as e:
      app.logger.error(f"Failed to upload: {e}")
      return jsonify({"error": "Failed to upload"}), 500
    return jsonify(unverified_data), 200


def addLabelHandler(label):
    if label not in Labels:
        Labels.append(label)  # Tentatively add the label
        try:
            if not os.path.isfile(labelsJSON):
                with open(labelsJSON, 'w') as file:
                    json.dump([], file)
            with open(labelsJSON, 'r') as file:
                existing_labels = json.load(file)
            existing_labels.append(label)
            with open(labelsJSON, 'w') as file:
                json.dump(existing_labels, file)   
            return
        except Exception as e:
            if label in Labels:
                Labels.remove(label)
            return
    else:
        return "Label already exists"

@app.route('/addLabel', methods=["POST"])
def addLabel():
  newLabel = request.data.decode('utf-8').strip()
  addLabelHandler(newLabel)
  print(Labels)
  return Labels

def sendFileToS3():
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


x = getInitialData()
if __name__ == '__main__':
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    app.run(port=port, debug=True)



    

# @app.route('/upload', methods=["GET", "POST"])
# def upload():
#   if request.method == "GET":
#     return '''
#       <form action="/upload" method="post" enctype="multipart/form-data">
#         <input type="file" name="file">
#         <input type="submit" value="Upload">
#       </form>
#           '''
#   elif request.method == "POST":
#     file = request.files["file"]
#     file.save(os.path.join(UNVERIFIED_BUCKET, file.filename))
#     return "do not test this page"
