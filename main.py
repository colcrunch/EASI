import sqlite3 as sql
import flask
from flask import abort, redirect, url_for
from flask import render_template
from flask import Flask
easi = Flask(__name__)

@easi.route('/')
def index():
    return render_template('index.html')

@easi.route('/api')
def api():
    return redirect(url_for('index'))

@easi.errorhandler(404)
def notfound(error):
    return 'This is not the page you are looking for.'
