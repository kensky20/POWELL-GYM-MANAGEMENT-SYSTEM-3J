import json, os, threading
from datetime import date
BASE=os.path.dirname(os.path.abspath(__file__))
MEMBERS=os.path.join(BASE,"powell_gym_data.json")
USERS=os.path.join(BASE,"users.json")
LOCK=threading.Lock()
def read(path, default):
    if not os.path.exists(path):
        write(path,default); return default
    try:
        with open(path,encoding="utf-8") as f: return json.load(f)
    except (OSError,json.JSONDecodeError): return default
def write(path,data):
    temp=path+".tmp"
    with open(temp,"w",encoding="utf-8") as f: json.dump(data,f,indent=4)
    os.replace(temp,path)
def get_members():
    with LOCK: return read(MEMBERS,[])
def save_members(rows):
    with LOCK: write(MEMBERS,rows)
def next_member_id(rows):
    nums=[]
    for m in rows:
        try: nums.append(int(m["member_id"].replace("PG-","")))
        except (ValueError,KeyError): pass
    return f"PG-{max(nums,default=0)+1:04d}"
def membership_status(start,end):
    today=date.today()
    if today<date.fromisoformat(start): return "Upcoming"
    if today>date.fromisoformat(end): return "Expired"
    return "Active"
def initialize_files():
    with LOCK:
        if not os.path.exists(MEMBERS): write(MEMBERS,[])
        if not os.path.exists(USERS): write(USERS,[{"username":"admin","password":"admin123"}])
