import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import redirect, url_for, render_template, request
from flask_dance.contrib.google import make_google_blueprint, google
from werkzeug.utils import secure_filename
from app import app

UPLOAD_FOLDER = '/upload-file'
ALLOWED_EXTENSIONS = set(['zip', 'rar'])


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
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload-files", methods=['GET', 'POST'])
def upfiles():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload-file',
                                    filename=filename))

    return render_template('upload')
