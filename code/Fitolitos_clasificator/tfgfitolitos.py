from flask import Flask, redirect, url_for
from flask_dance.contrib.dropbox import make_dropbox_blueprint, dropbox

app = Flask(__name__)
app.secret_key = "supersekrit"
blueprint = make_dropbox_blueprint(
    app_key="tza9hqk0moy3rh4",
    app_secret="30jofh5613jmlex",
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not dropbox.authorized:
        return redirect(url_for("dropbox.login"))
    resp = dropbox.post("users/get_current_account")
    assert resp.ok
    return "You are {email} on Dropbox".format(email=resp.json()["email"])
if __name__ == "__main__":
    app.run()

