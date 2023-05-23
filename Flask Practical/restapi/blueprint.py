from flask import Blueprint,Flask

app = Flask(__name__)

rest_blueprint = Blueprint('rest_blueprint',__name__,url_prefix='/rest')