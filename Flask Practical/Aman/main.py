# from app_config import app
from flask import Flask
from api import user_blueprint
# from restapi.blueprint import rest_blueprint
from product_api import product_blueprint
from rest_api import rest_blueprint
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.secret_key = b"ghjkjlkgfdfghjkl98797980989jhgfghjkl"

app.config["JWT_SECRET_KEY"]= "jjdkjads834dmdk7"

jwt = JWTManager(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(rest_blueprint)


if __name__ == '__main__':
    app.run(debug=True,port=8000)