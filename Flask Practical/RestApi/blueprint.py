from flask import Blueprint
from api import ProductApiView,ProductAPi
from app import app


flask_blueprint = Blueprint('my_blueprint', __name__,url_prefix='/api')

my_view = ProductApiView.as_view('my_view')
my_view2 = ProductAPi.as_view('my_view2')


flask_blueprint.add_url_rule('/product',view_func=my_view)
flask_blueprint.add_url_rule('/product/<int:id>',view_func=my_view2)





app.register_blueprint(flask_blueprint)
if __name__ == '__main__':
    app.run(debug=True,port=8000)