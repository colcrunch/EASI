import sqlite3 as sql
import flask
import memcache
from flask import abort, redirect, url_for
from flask import render_template
from flask import Flask
import cron.test as test

easi = Flask(__name__)

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

@easi.route('/')
def index():
    return render_template('index.html')

@easi.route('/api')
def api():
    return redirect(url_for('index'))

@easi.route('/api/killsDaily/')
def getKillsDaily():
    result = test.help()
    return result

@easi.route('/l')
def xache():
    if mc.get('test'):
        ll = mc.get('test')
        return 'True'+ ll
    elif not mc.get('test'):
        t = test.help()
        return 'False'+t
    else:
        return 'Error'

@easi.errorhandler(404)
def notfound(error):
    return 'This is not the page you are looking for.'

if __name__ == "__main__":
    easi.run()
