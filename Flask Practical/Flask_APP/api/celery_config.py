from flask import Flask
from flask_mail import Mail, Message
from celery import Celery, shared_task
from celery.schedules import crontab
import pymysql as Pymysqldb


def MysqlDB():
    conn = Pymysqldb.connect(
    host = 'localhost',
    user = 'root',
    password = 'Dubey@123',
    database = 'FlaskDB',
    )
    return conn

flask_app = Flask(__name__)
flask_app.config['MAIL_SERVER'] = 'smtp.gmail.com'
flask_app.config['MAIL_PORT'] = 465
flask_app.config['MAIL_USERNAME'] = 'amandubey@simprosys.com'
flask_app.config['MAIL_PASSWORD'] = 'zsuoyovnmxuqceam'
flask_app.config['MAIL_USE_TLS'] = False
flask_app.config['MAIL_USE_SSL'] = True



flask_app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
flask_app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
flask_app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'

# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_TIMEZONE = 'Asia/Kolkata'

mail = Mail(flask_app)


def make_celery(app):
    celery = Celery(app.import_name, broker=flask_app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(flask_app)


@shared_task()
def send_mail_to_user():
    print("________________________________-")
    with flask_app.app_context():
        conn = MysqlDB()
        mycursor = conn.cursor()
        mycursor.execute("SELECT email FROM users")
        result = mycursor.fetchall()
        emails = [r[0] for r in result]
        print('emails',emails)
        for email in emails:
            msg = Message('Thank you for joining', sender='satyawann@simprosys.com', recipients=[email])
            msg.body = f"Welcome to our community! We're thrilled to have you join us and can't wait to see what you bring to the table. Don't hesitate to reach out if you have any questions or if there's anything we can do to help make your experience here even better {email}"
            mail.send(msg)
        return 'Send Email Successfully'



celery.conf['CELERYBEAT_SCHEDULE'] = {
    'send-mail-to-user': {
        'task': 'celery_config.send_mail_to_user',
        'schedule':crontab(minute='*/1')
    },
}

if __name__ == '__main__':
    celery.conf.timezone = 'Asia/Kolkata'
    with flask_app.app_context():
        celery.conf.update(flask_app.config)
    flask_app.run(debug=True)