import os

from oauthlib.oauth2 import InvalidGrantError, TokenExpiredError, InvalidClientIdError

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
    try:
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
    except (InvalidGrantError, TokenExpiredError, InvalidClientIdError) as e:
        return redirect(url_for("google.login"))
    return render_template('index.html', email=resp.json()["email"])


@app.route("/upload-files")
def upfiles():
    target = os.path.join(UPLOAD_FOLDER, 'images/')
    image_names = os.listdir(target)
    print(image_names)
    return render_template("upload",image_names=image_names )


@app.route('/etiquetador', methods=['GET', 'POST'])
def annotator():
    target = os.path.join(UPLOAD_FOLDER, 'images/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for upload in request.files.getlist("file"):
        filename = upload.filename
        print(filename)
        destination = "/".join([target, filename])
        upload.save(destination)
    image_names = os.listdir(target)
    print(image_names)
    return render_template("etiquetador.html", image_names=image_names)

@app.route('/upload-files/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    return render_template("show_images.html", image_names=image_names)