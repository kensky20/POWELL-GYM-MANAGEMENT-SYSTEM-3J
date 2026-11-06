import tkinter as tk
from tkinter import messagebox
import json,os
class LoginWindow:
    def __init__(self,root,on_success):
        self.root=root; self.on_success=on_success
        self.users=os.path.join(os.path.dirname(os.path.abspath(__file__)),"users.json")
        root.title("Powell Gym - Login"); root.geometry("430x500"); root.resizable(False,False); root.configure(bg="#eef2f7")
        box=tk.Frame(root,bg="white",padx=35,pady=30); box.place(relx=.5,rely=.5,anchor="center",width=350,height=400)
        tk.Label(box,text="POWELL POWER",bg="white",fg="#172554",font=("Arial",19,"bold")).pack(pady=(8,0))
        tk.Label(box,text="WELLNESS GYM",bg="white",fg="#64748b").pack(pady=(0,25))
        tk.Label(box,text="Username",bg="white").pack(anchor="w")
        self.user=tk.Entry(box,font=("Arial",11)); self.user.pack(fill="x",ipady=8,pady=(5,15))
        tk.Label(box,text="Password",bg="white").pack(anchor="w")
        self.password=tk.Entry(box,font=("Arial",11),show="*"); self.password.pack(fill="x",ipady=8,pady=5)
        self.show=tk.BooleanVar()
        tk.Checkbutton(box,text="Show password",variable=self.show,command=lambda:self.password.config(show="" if self.show.get() else "*"),bg="white").pack(anchor="w")
        tk.Button(box,text="LOG IN",command=self.login,bg="#1d4ed8",fg="white",relief="flat").pack(fill="x",ipady=10,pady=20)
        tk.Label(box,text="Default login: admin / admin123",bg="white",fg="#64748b",font=("Arial",8)).pack()
        root.bind("<Return>",lambda e:self.login())
    def login(self):
        u=self.user.get().strip(); p=self.password.get()
        if not u or not p: return messagebox.showwarning("Required","Enter username and password.")
        try:
            with open(self.users,encoding="utf-8") as f: users=json.load(f)
        except Exception: return messagebox.showerror("Error","Cannot read users.json.")
        if any(x.get("username")==u and x.get("password")==p for x in users):
            self.root.unbind("<Return>"); self.on_success(u)
        else:
            messagebox.showerror("Login Failed","Incorrect username or password."); self.password.delete(0,"end")
