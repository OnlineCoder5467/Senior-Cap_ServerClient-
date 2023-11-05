# Senior-Cap_ServerClient-

To launch debug server at local port 5000 in Windows, first:

(1) create a virtual environment at the root folder

.\Scripts\Activate.ps1
(you can now test locally, you may have to install the dependencies)

(2) cmd: pip install flask

(3) navigate to Scripts directory

note: you may have to install dotenv with cmd: pip install dotenv

10/12 ADDED MODULE: Flask-Cors 4.0.0

(4) cmd: flask run



To launch using Docker
docker build -t your-image-name:tag .
docker run -d --name your-image-name:tag -p 5000:5000 your-image-name:tag

to stop
docker stop your-image-name:tag

If you're just working locally any name will do, no need to tag, remember the period .
