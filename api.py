import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
from datetime import date
from database import get_members,save_members,next_member_id,membership_status
HOST,PORT="127.0.0.1",8765
FIELDS=["full_name","age","gender","contact_number","address","membership_type","start_date","expiration_date"]
def validate_member(d):
    for k in FIELDS:
        if not str(d.get(k,"")).strip(): return k.replace("_"," ").title()+" is required."
    name=str(d["full_name"]).strip()
    if len(name)<2 or len(name)>100 or not all(c.isalpha() or c in " .'-" for c in name): return "Enter a valid full name."
    try:
        age=int(d["age"])
        if not 1<=age<=120: return "Age must be between 1 and 120."
    except (ValueError,TypeError): return "Age must be a whole number."
    if d["gender"] not in ["Male","Female","Other"]: return "Select a valid gender."
    phone=str(d["contact_number"]).strip()
    if not(phone.startswith("09") and phone.isdigit() and len(phone)==11): return "Contact number must use 09XXXXXXXXX format."
    if len(str(d["address"]))>255: return "Address must not exceed 255 characters."
    if d["membership_type"] not in ["Daily","Weekly","Monthly","Quarterly","Yearly"]: return "Select a valid membership type."
    try:
        if date.fromisoformat(d["expiration_date"])<date.fromisoformat(d["start_date"]): return "Expiration date cannot be earlier than start date."
    except (ValueError,TypeError): return "Dates must use YYYY-MM-DD format."
    return None
class Handler(BaseHTTPRequestHandler):
    def send_data(self,code,obj):
        raw=json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def get_body(self):
        size=int(self.headers.get("Content-Length",0))
        if size>1000000: raise ValueError("Request too large.")
        return json.loads(self.rfile.read(size).decode() or "{}")
    def do_GET(self):
        p=urlparse(self.path)
        if p.path=="/health": return self.send_data(200,{"success":True,"message":"API running"})
        if p.path!="/members": return self.send_data(404,{"success":False,"message":"Endpoint not found."})
        q=parse_qs(p.query).get("q",[""])[0].lower()
        rows=get_members()
        if q: rows=[m for m in rows if q in m.get("member_id","").lower() or q in m.get("full_name","").lower()]
        self.send_data(200,{"success":True,"data":rows})
    def do_POST(self):
        if urlparse(self.path).path!="/members": return self.send_data(404,{"success":False,"message":"Not found"})
        try:
            d=self.get_body(); err=validate_member(d)
            if err: return self.send_data(400,{"success":False,"message":err})
            rows=get_members(); m={k:str(d[k]).strip() for k in FIELDS}
            m["member_id"]=next_member_id(rows); m["status"]=membership_status(m["start_date"],m["expiration_date"])
            rows.append(m); save_members(rows)
            self.send_data(201,{"success":True,"message":"Member added successfully.","data":m})
        except Exception as e: self.send_data(400,{"success":False,"message":str(e)})
    def do_PUT(self):
        p=urlparse(self.path).path.strip("/").split("/")
        if len(p)!=2 or p[0]!="members": return self.send_data(404,{"success":False,"message":"Not found"})
        try:
            d=self.get_body(); err=validate_member(d)
            if err: return self.send_data(400,{"success":False,"message":err})
            rows=get_members()
            for i,old in enumerate(rows):
                if old.get("member_id")==p[1]:
                    m={k:str(d[k]).strip() for k in FIELDS}; m["member_id"]=p[1]; m["status"]=membership_status(m["start_date"],m["expiration_date"])
                    rows[i]=m; save_members(rows)
                    return self.send_data(200,{"success":True,"message":"Member updated successfully.","data":m})
            self.send_data(404,{"success":False,"message":"Member not found."})
        except Exception as e: self.send_data(400,{"success":False,"message":str(e)})
    def do_DELETE(self):
        p=urlparse(self.path).path.strip("/").split("/")
        if len(p)!=2 or p[0]!="members": return self.send_data(404,{"success":False,"message":"Not found"})
        rows=get_members(); new=[m for m in rows if m.get("member_id")!=p[1]]
        if len(rows)==len(new): return self.send_data(404,{"success":False,"message":"Member not found."})
        save_members(new); self.send_data(200,{"success":True,"message":"Member deleted successfully."})
    def log_message(self,*args): pass
def run_server(): ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()
if __name__=="__main__": run_server()
