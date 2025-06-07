from flask import Flask
from flask_kerberos import requires_authentication

app = Flask(__name__)

@app.route("/")
@requires_authentication
def index(user):
    return f"Hello, {user}"

app.run(host="0.0.0.0", port=8000)

