import os
from flask import Flask, request
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

UPLOAD_FOLDER = '../imagebucket/'

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


if __name__ == "__main__":
  app.run()