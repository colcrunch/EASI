from flask import Flask
easi = Flask(__name__)

@easi.route('/')
def hello():
    return 'Hello, World!'

@easi.route('/api')
def api():
    return 'Api Goes Here.'
