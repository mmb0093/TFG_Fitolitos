from flask import Flask, redirect, url_for
from werkzeug.contrib.fixers import ProxyFix
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id="281827376141-o7jg2rs9knjkgav5ej8bjst33bhuqn9k.apps.googleusercontent.com",
    client_secret="3Zsil8hOEc_NEGuZDZOkMIv4",
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/user")
    assert resp.ok
    return "You are @{login} on Google".format(login=resp.json()["login"])

if __name__ == "__main__":
	app.run(host='0.0.0.0')
