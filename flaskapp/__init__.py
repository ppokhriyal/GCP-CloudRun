from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Welcome to GCP Cloud Run</h1>"
