# from flask import Flask,render_template,request,session,redirect,url_for,Blueprint
# import pymysql as Pymysqldb
# # import MySQLdb
# # import MySQLdb.cursors
# import mysql.connector
# from flask_mail import Mail,Message
# import random
# import string
# import csv
# from io import StringIO
# import threading

# app = Flask(__name__,template_folder="/Users/simprosysinfomedia/Desktop/Aman/Flask Practical/Flask_APP/templates/")
# app.secret_key = b'ghjkjlkgfdfghjkl98797980989jhgfghjkl'


# my_blueprint = Blueprint('my_blueprint',__name__,url_prefix='/api')
# app.register_blueprint(my_blueprint)


# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT']= 587
# app.config['MAIL_USERNAME'] = 'amandubey@simprosys.com'
# app.config['MAIL_PASSWORD'] = 'zsuoyovnmxuqceam'
# app.config['MAIL_USE_TLS'] = True

# mail = Mail(app)


# def MysqlDB():
#     conn = Pymysqldb.connect(
#     host = 'localhost',
#     user = 'root',
#     password = '1234',
#     database = 'FlaskDB',
#     )
#     return conn



# def savecsv():
#     return "HELLO"

# @app.route('/savecsv',methods=['POST','GET'])
# def savecsvusinghread():
#     t = threading.Thread(target=savecsv)
#     t.start()
#     t.join()
#     return render_template('csv.html')



# if __name__ == '__main__':
#     app.run(debug=True,port=8000)