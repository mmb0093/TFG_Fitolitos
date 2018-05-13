import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import redirect, url_for, render_template, request, make_response, flash, send_from_directory
from flask_dance.contrib.google import make_google_blueprint, google
from app import app

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))



app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id = "927801431905-5kajpv4ihkctidgn1p5l4ctkfmrepnq6.apps.googleusercontent.com",
    client_secret = "sTqxZsqTWgDj7oMTISS_FuUn",
    scope = ["profile", "email"],
    reprompt_consent=True,
)
app.register_blueprint(blueprint, url_prefix="/login")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")

    assert resp.ok, resp.text
    return render_template('index.html', email=resp.json()["email"])


@app.route("/upload-files", methods=['GET', 'POST'])
def upfiles():
    target = os.path.join(UPLOAD_FOLDER, 'images/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    print("hola fuera")
    for upload in request.files.getlist("file"):
        filename = upload.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("hola")
        print("Save it to:", destination)
        upload.save(destination)
    return render_template("upload", )


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    return render_template("show_images.html", image_names=image_names)