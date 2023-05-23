from flask import Flask,Blueprint

product_blueprint = Blueprint('product_blueprint', __name__,url_prefix='/product')

app = Flask(__name__)