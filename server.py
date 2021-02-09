from flask import Flask
app = Flask(__name__)


@app.route('/')
def get_root_dir():
    return 'hello world';