from flask import Flask
from celery_config import celery_app

app = Flask(__name__)
celery_app.conf.update(app.config)

@app.route("/")
def index():
    result = celery_app.send_task('my_app.tasks.add_numbers', args=[2, 3])
    return f"Result: {result.get()}"



if __name__ == '__main__':
    app.run(debug=True)  