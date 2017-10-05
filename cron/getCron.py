import datetime
import sqlite3 as sql
import requests
import re
import json
import os.path

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sde_path = database_path = os.path.join(app_dir, 'sde.db')
db_path  = database_path = os.path.join(app_dir, 'data.db')

def regexp(pattern, input):
    return bool(re.match(pattern, input))

time = datetime.datetime.utcnow().strftime("%Y-%d-%m %H")

regg = '[Jj]([0-9]{6})'
conn = sql.connect(sde_path)
conn.create_function("regexp", 2, regexp)
c = conn.cursor()
c.execute("SELECT solarSystemID from mapSolarSystems WHERE solarSystemName NOT regexp :pattern", {'pattern': regg})
sysids = c.fetchall()
print(len(sysids))
conn.close()

urlk = "https://esi.tech.ccp.is/latest/universe/system_kills/?datasource=tranquility"
headers = {'user-agent': 'application: https://github.com/colcrunch/killbot contact: rhartnett35@gmail.com','content-type': 'application/json'}
r = requests.get(urlk, headers=headers)
kills = r.json()
conn = sql.connect(db_path)
c = conn.cursor()

ktotal = []
kids = []
for x in kills:
    sys = x["system_id"]
    skills = x["ship_kills"]
    nkills = x["npc_kills"]
    pkills = x["pod_kills"]

    ktotal.append((sys, skills, nkills, pkills, time))
    kids.append(sys)

for sysid in sysids:
    if sysid[0] not in kids:
        ktotal.append((sysid[0], 0, 0, 0, time))
    else:
        pass

c.executemany('INSERT INTO kills (system, ship_kills, npc_kills, pod_kills, dt) VALUES (?,?,?,?,?)',ktotal)
conn.commit()


urlk = "https://esi.tech.ccp.is/latest/universe/system_jumps/?datasource=tranquility"
headers = {'user-agent': 'application: https://github.com/colcrunch/killbot contact: rhartnett35@gmail.com','content-type': 'application/json'}
r = requests.get(urlk, headers=headers)
jumps = r.json()


jtotal = []
jids = []
for x in jumps:
    sys = x["system_id"]
    sjumps = x["ship_jumps"]

    jtotal.append((sys, sjumps, time))
    jids.append(sys)

for sysid in sysids:
    if sysid[0] not in jids:
        jtotal.append((sysid[0], 0, time))
    else:
        pass

c.executemany('INSERT INTO jumps (system, jumps, dt) VALUES (?,?,?)',jtotal)
conn.commit()
conn.close()
print(time)
print("Database updated")
