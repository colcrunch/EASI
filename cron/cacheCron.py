import datetime
import sqlite3 as sql
import requests
import re
import json
import os.path
import memcache
from collections import OrderedDict

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sde_path = database_path = os.path.join(app_dir, 'sde.db')
db_path  = database_path = os.path.join(app_dir, 'data.db')

def respDaily():
    ye = datetime.datetime.now() - datetime.timedelta(days=1)
    yeStr = "%2017-05-10%"
    tom = datetime.datetime.now() + datetime.timedelta(days=1)
    conn = sql.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT system, sum(ship_kills) as ship_kills, sum(npc_kills) as npc_kills, sum(pod_kills) as pod_kills FROM kills WHERE dt LIKE ? GROUP BY system",(yeStr,))
    r = c.fetchall()
    print(len(r))

    response = []
    for result in r:
        tmp = OrderedDict(zip(['system', 'ship_kills', 'npc_kills', 'pod_kills'],[result[0], result[1],result[2],result[3]]))
        response.append(tmp)

    print(response)
    obj =  mc.get("killsDaily")
    if not obj:
        mc.set("killsDaily", response)
    else:
        mc.delete("killsDaily")
        mc.set("killsDaily", response)

    obj2 = mc.get('dailyExp')
    if not obj2:
        mc.set("dailyExp", tom.isoformat())
    else:
        mc.delete("dailyExp")
        mc.set("dailyExp", tom.isoformat())

if __name__ == '__main__':
    import sys
    function = getattr(sys.modules[__name__], sys.argv[1])
    function()
