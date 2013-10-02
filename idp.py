import json
import time

from flask import Flask, render_template, abort, jsonify
from flask.ext.login import LoginManager, UserMixin, login_required, current_user
import bcrypt
import settings
from browserid.jwt import generate, load_key

app = Flask(__name__)
app.config.from_object(settings)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
  @classmethod
  def get(cls, email):
    with open("users.json") as f:
      users = json.load(f)

    if users.get(email):
      return User(email, users[email]["hash"], users[email]["salt"])
    else:
      return None

  def __init__(self, email, hash, salt):
    self.email = unicode(email)
    self.hash = hash
    self.salt = salt

  def get_id(self):
    return self.email

  def verify_password(self, password):
    return bcrypt.hashpw(password, self.salt) == self.hash


def make_email(username):
  return username + "@" + app.config["DOMAIN"]


@app.before_request
def before_request():
  app.jinja_env.globals["DOMAIN"] = app.config["DOMAIN"]


@app.route("/provisioning")
def provisioning():
  return render_template("provisioning.html")


@app.route("/authentication")
def authentication():
  return render_template("authentication.html")


@app.route("/login", methods=["POST"])
def pwlogin():
  username = request.form["username"]
  password = request.form["password"]
  email = make_email(username)
  user = User.get(email)
  if not user:
    return abort(403)

  if user.verify_password(password):
    login_user(user, remember=True)
    return "ok"
  else:
    return abort(403)


@app.route("/2fa")
def twofa():
  pass


@app.route("/signcert", methods=["POST"])
@login_required
def signcert():
  email = request.json.get("email")
  duration = request.json.get("certDuration")
  public_key = request.json.get("publicKey")

  if not email or not duration or not public_key or email != current_user.email:
    return abort(400)

  now = time.time()
  expiry_time = int(now + float(duration)) * 1000

  with open("key.json") as f:
    k = json.load(f)

  key = load_key("RS256", k)
  data = {
    "iss": app.config["DOMAIN"],
    "exp": expiry_time,
    "iat": int(now) * 1000,
    "public-key": public_key,
    "principal": {"email": current_user.email}
  }

  signed_data = generate(data, key)
  return jsonify(certificate=signed_data)


@app.route("/logout")
@login_required
def logout():
  logout_user()
  return "ok"


if app.debug:
  @app.route("/test_login")
  def test_login():
    return render_template("test_login.html")


if __name__ == "__main__":
  import sys

  if app.debug and len(sys.argv) > 1:
    if sys.argv[1] == "add":
      import getpass
      username = raw_input("Username: ").strip().lower()
      email = make_email(username)
      password = getpass.getpass()
      salt = bcrypt.gensalt()
      hash = bcrypt.hashpw(password, salt)
      with open("users.json") as f:
        users = json.load(f)

      users[email] = {"hash": hash, "salt": salt}

      with open("users.json", "w") as f:
        json.dump(users, f)

      print "Added user {}".format(email)
    elif sys.argv[1] == "del":
      username = raw_input("Username: ").strip().lower()
      email = make_email(username)
      with open("users.json") as f:
        users = json.load(f)

      users.pop(email, None)

      with open("users.json", "w") as f:
        json.dump(users, f)
      print "Removed user {}".format(email)

  else:
    if app.debug:
      app.run(debug=True, host="", port=app.config["PORT"])
    else:
      from gevent.wsgi import WSGIServer
      from werkzeug.contrib.fixers import ProxyFix
      app.wsgi_app = ProxyFix(app.wsgi_app)
      server = WSGIServer((app.config["HOST"], app.config["PORT"]), app)
      server.serve_forever()

