from flask import Flask,Blueprint

user_blueprint = Blueprint('user_blueprint', __name__,url_prefix="user")

app = Flask(__name__)