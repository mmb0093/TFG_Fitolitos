import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id="927801431905-5kajpv4ihkctidgn1p5l4ctkfmrepnq6.apps.googleusercontent.com",
    client_secret="KfS0AD-25Q0yp-GfbSww874C",
    scope=["profile", "email"],
    offline=True,
    #redirect_url='/',
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
    # app.run(host='0.0.0.0')



