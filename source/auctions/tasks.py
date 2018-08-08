from celery import Celery

app = Celery('yaas5_project', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y