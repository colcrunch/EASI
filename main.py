import flask
import memcache
from flask import abort, redirect, url_for
from flask import render_template
from flask import Flask, Blueprint
import cron.test as test
import json
from flask_restplus import Resource, Api, fields

easi = Flask(__name__)
api_p = Blueprint('api', __name__,  url_prefix='/api')
api = Api(api_p, version='1.0', title='EVE Aggregate Statistics Interface', description='Aggregate Statistics gathered from ESI.',)

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

kills = api.namespace("kills", description="Kill stats")

@easi.route('/')
def doc():
    return redirect(url_for('api.doc'))

@kills.route('/killsDaily')
class KillsDaily(Resource):
    def get(self):
            res = json.dumps(mc.get("killsDaily"))
            exp = mc.get("dailyExp")
            result = flask.Response(res)
            result.headers['expires'] = mc.get("dailyExp")
            result.headers['content-type'] = "application/json"
            return result

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == "__main__":
    easi.register_blueprint(api_p)
    easi.run(debug=True)
