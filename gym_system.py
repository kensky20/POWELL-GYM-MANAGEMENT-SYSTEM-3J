import tkinter as tk
from tkinter import ttk, messagebox
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
import json

API = "http://127.0.0.1:8765"

def api_request(path, method="GET", data=None):
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = Request(API + path, data=body, method=method,
                  headers={"Content-Type":"application/json"})
    try:
        with urlopen(req, timeout=4) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        try: raise Exception(json.loads(error.read().decode("utf-8")).get("message","API error"))
        except json.JSONDecodeError: raise Exception(f"API error {error.code}")
    except URLError: raise Exception("Cannot connect to the local API. Close and restart the app.")

class GymDashboard:
    def __init__(self, root, username, on_logout):
        self.root=root; self.username=username; self.on_logout=on_logout; self.selected_id=None
        root.title("Powell Power Wellness Gym - Membership Management")
        root.geometry("1200x720"); root.minsize(1000,640); root.configure(bg="#f1f5f9")
        self.sidebar=tk.Frame(root,bg="#172554",width=215); self.sidebar.pack(side="left",fill="y"); self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar,text="POWELL POWER",bg="#172554",fg="white",font=("Arial",16,"bold")).pack(pady=(28,0))
        tk.Label(self.sidebar,text="WELLNESS GYM",bg="#172554",fg="#bfdbfe",font=("Arial",9,"bold")).pack(pady=(0,35))
        self.nav("Dashboard",self.show_dashboard); self.nav("Membership Records",self.show_members)
        tk.Label(self.sidebar,text="Logged in: "+username,bg="#172554",fg="#cbd5e1").pack(side="bottom",pady=8)
        tk.Button(self.sidebar,text="LOG OUT",command=self.logout,bg="#b91c1c",fg="white",relief="flat").pack(side="bottom",fill="x",padx=16,pady=12,ipady=8)
        self.content=tk.Frame(root,bg="#f1f5f9"); self.content.pack(side="right",fill="both",expand=True)
        self.show_dashboard()
    def nav(self,label,command):
        tk.Button(self.sidebar,text=label,command=command,anchor="w",bg="#1e3a8a",fg="white",activebackground="#2563eb",relief="flat",font=("Arial",10,"bold"),padx=18).pack(fill="x",padx=12,pady=5,ipady=12)
    def clear(self):
        for w in self.content.winfo_children(): w.destroy()
    def title(self,name,sub):
        tk.Label(self.content,text=name,bg="#f1f5f9",fg="#0f172a",font=("Arial",22,"bold")).pack(anchor="w",padx=26,pady=(22,2))
        tk.Label(self.content,text=sub,bg="#f1f5f9",fg="#64748b").pack(anchor="w",padx=26,pady=(0,15))
    def members(self,q=""):
        suffix="?"+urlencode({"q":q}) if q else ""
        return api_request("/members"+suffix)["data"]
    def show_dashboard(self):
        self.clear(); self.title("Dashboard","Membership overview")
        try:
            rows=self.members()
            values=[("Total Members",len(rows)),("Active",sum(x["status"]=="Active" for x in rows)),("Expired",sum(x["status"]=="Expired" for x in rows)),("Upcoming",sum(x["status"]=="Upcoming" for x in rows))]
            wrap=tk.Frame(self.content,bg="#f1f5f9"); wrap.pack(fill="x",padx=18,pady=10)
            for label,value in values:
                card=tk.Frame(wrap,bg="white",padx=20,pady=18,highlightbackground="#e2e8f0",highlightthickness=1)
                card.pack(side="left",expand=True,fill="x",padx=7)
                tk.Label(card,text=label,bg="white",fg="#64748b",font=("Arial",10,"bold")).pack(anchor="w")
                tk.Label(card,text=str(value),bg="white",fg="#1d4ed8",font=("Arial",26,"bold")).pack(anchor="w",pady=(8,0))
            tk.Label(self.content,text="Welcome to Powell Power Wellness Gym.",bg="#f1f5f9",fg="#334155",font=("Arial",13)).pack(anchor="w",padx=28,pady=25)
            tk.Label(self.content,text="Select Membership Records to add, view, search, update, or delete member records.",bg="#f1f5f9",fg="#64748b").pack(anchor="w",padx=28)
        except Exception as e: messagebox.showerror("API Error",str(e))
    def show_members(self):
        self.clear(); self.title("Membership Records","Add, search, update, and delete gym members")
        panel=tk.Frame(self.content,bg="white",padx=12,pady=10); panel.pack(fill="x",padx=22,pady=(0,10))
        self.entries={}
        fields=[("Full Name","full_name"),("Age","age"),("Contact Number","contact_number"),("Address","address"),("Start Date YYYY-MM-DD","start_date"),("Expiration Date YYYY-MM-DD","expiration_date")]
        for i,(label,key) in enumerate(fields):
            r,c=divmod(i,3); cell=tk.Frame(panel,bg="white"); cell.grid(row=r,column=c,padx=7,pady=5,sticky="ew")
            tk.Label(cell,text=label,bg="white",fg="#334155",font=("Arial",9,"bold")).pack(anchor="w")
            entry=tk.Entry(cell,font=("Arial",10),relief="solid",bd=1); entry.pack(fill="x",ipady=5,pady=(3,0)); self.entries[key]=entry
        for c in range(3): panel.grid_columnconfigure(c,weight=1)
        options=tk.Frame(panel,bg="white"); options.grid(row=2,column=0,columnspan=3,sticky="w",padx=7,pady=5)
        tk.Label(options,text="Gender",bg="white").pack(side="left")
        self.gender=tk.StringVar(value="Male")
        ttk.Combobox(options,textvariable=self.gender,values=["Male","Female","Other"],state="readonly",width=12).pack(side="left",padx=(7,22))
        tk.Label(options,text="Membership",bg="white").pack(side="left")
        self.kind=tk.StringVar(value="Monthly")
        ttk.Combobox(options,textvariable=self.kind,values=["Daily","Weekly","Monthly","Quarterly","Yearly"],state="readonly",width=14).pack(side="left",padx=7)
        actions=tk.Frame(panel,bg="white"); actions.grid(row=3,column=0,columnspan=3,sticky="w",padx=7,pady=8)
        self.button(actions,"ADD MEMBER",self.add,"#15803d"); self.button(actions,"UPDATE",self.update,"#1d4ed8"); self.button(actions,"DELETE",self.delete,"#b91c1c"); self.button(actions,"CLEAR",self.clear_form,"#475569")
        search=tk.Frame(self.content,bg="#f1f5f9"); search.pack(fill="x",padx=22,pady=5)
        tk.Label(search,text="Search ID or name:",bg="#f1f5f9").pack(side="left")
        self.query=tk.Entry(search,width=28); self.query.pack(side="left",padx=8,ipady=4)
        self.button(search,"SEARCH",self.search,"#334155"); self.button(search,"SHOW ALL",self.load_table,"#64748b")
        holder=tk.Frame(self.content,bg="white"); holder.pack(fill="both",expand=True,padx=22,pady=(5,18))
        cols=("id","name","age","gender","contact","type","start","end","status")
        self.tree=ttk.Treeview(holder,columns=cols,show="headings",height=10)
        heads=["Member ID","Full Name","Age","Gender","Contact","Membership","Start Date","Expiration","Status"]
        widths=[85,150,45,65,105,90,90,95,75]
        for col,head,width in zip(cols,heads,widths):
            self.tree.heading(col,text=head); self.tree.column(col,width=width,anchor="center")
        scroll=ttk.Scrollbar(holder,orient="vertical",command=self.tree.yview); self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left",fill="both",expand=True); scroll.pack(side="right",fill="y")
        self.tree.bind("<<TreeviewSelect>>",self.select_row); self.load_table()
    def button(self,parent,label,cmd,color):
        tk.Button(parent,text=label,command=cmd,bg=color,fg="white",relief="flat",cursor="hand2",font=("Arial",8,"bold"),padx=11,pady=7).pack(side="left",padx=(0,6))
    def form(self):
        return {"full_name":self.entries["full_name"].get().strip(),"age":self.entries["age"].get().strip(),"gender":self.gender.get(),"contact_number":self.entries["contact_number"].get().strip(),"address":self.entries["address"].get().strip(),"membership_type":self.kind.get(),"start_date":self.entries["start_date"].get().strip(),"expiration_date":self.entries["expiration_date"].get().strip()}
    def load_table(self,rows=None):
        try:
            if rows is None: rows=self.members()
            for item in self.tree.get_children(): self.tree.delete(item)
            for m in rows: self.tree.insert("","end",values=(m["member_id"],m["full_name"],m["age"],m["gender"],m["contact_number"],m["membership_type"],m["start_date"],m["expiration_date"],m["status"]))
        except Exception as e: messagebox.showerror("API Error",str(e))
    def add(self):
        try: 
            result=api_request("/members","POST",self.form()); messagebox.showinfo("Success",result["message"]); self.clear_form(); self.load_table()
        except Exception as e: messagebox.showerror("Cannot Add Member",str(e))
    def update(self):
        if not self.selected_id: return messagebox.showwarning("Select Member","Select a member from the table first.")
        try:
            result=api_request("/members/"+self.selected_id,"PUT",self.form()); messagebox.showinfo("Success",result["message"]); self.clear_form(); self.load_table()
        except Exception as e: messagebox.showerror("Cannot Update",str(e))
    def delete(self):
        if not self.selected_id: return messagebox.showwarning("Select Member","Select a member from the table first.")
        if not messagebox.askyesno("Confirm Delete","Delete member "+self.selected_id+"?"): return
        try:
            result=api_request("/members/"+self.selected_id,"DELETE"); messagebox.showinfo("Success",result["message"]); self.clear_form(); self.load_table()
        except Exception as e: messagebox.showerror("Cannot Delete",str(e))
    def search(self):
        try: self.load_table(self.members(self.query.get().strip()))
        except Exception as e: messagebox.showerror("Search Error",str(e))
    def select_row(self,event=None):
        selected=self.tree.selection()
        if not selected: return
        self.selected_id=self.tree.item(selected[0],"values")[0]
        try:
            m=next(x for x in self.members() if x["member_id"]==self.selected_id)
            for key in ["full_name","age","contact_number","address","start_date","expiration_date"]:
                self.entries[key].delete(0,"end"); self.entries[key].insert(0,m.get(key,""))
            self.gender.set(m["gender"]); self.kind.set(m["membership_type"])
        except Exception as e: messagebox.showerror("Selection Error",str(e))
    def clear_form(self):
        self.selected_id=None
        for e in self.entries.values(): e.delete(0,"end")
        self.gender.set("Male"); self.kind.set("Monthly")
        for item in self.tree.selection(): self.tree.selection_remove(item)
    def logout(self):
        if messagebox.askyesno("Log Out","Are you sure you want to log out?"):
            for w in self.root.winfo_children(): w.destroy()
            self.on_logout()
