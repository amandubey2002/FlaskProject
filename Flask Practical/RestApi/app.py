from flask import Flask
from flask_restful import marshal,fields,marshal_with,marshal_with_field,Api,Resource,request
# from blueprint import flask_blueprint
app = Flask(__name__)

api = Api(app)

# app.register_blueprint(flask_blueprint)


if __name__ == '__main__':
    app.run(debug=True,port=8000)