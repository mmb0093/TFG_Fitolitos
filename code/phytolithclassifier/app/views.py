import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import  redirect, url_for, render_template, request
from flask_dance.contrib.google import make_google_blueprint, google
from werkzeug.utils import secure_filename
from app import app

app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id="927801431905-5kajpv4ihkctidgn1p5l4ctkfmrepnq6.apps.googleusercontent.com",
    client_secret="KfS0AD-25Q0yp-GfbSww874C",
    scope=["profile", "email"],
    offline=True,
)
app.register_blueprint(blueprint, url_prefix="/login")




@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return render_template('index.html')



@app.route("/upload-files", methods=['GET', 'POST'])
def upfiles():
    return render_template('upload')
