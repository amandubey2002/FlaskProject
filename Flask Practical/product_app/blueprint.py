from flask import Blueprint,Flask
from app_config import app

# app = Flask(__name__)
product_blueprint = Blueprint('product_blueprint',__name__,url_prefix='/product')