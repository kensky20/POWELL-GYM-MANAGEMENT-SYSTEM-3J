import threading,time,tkinter as tk
from urllib.request import urlopen
from urllib.error import URLError
from database import initialize_files
from api import run_server
from login import LoginWindow
from gym_system import GymDashboard,API
def main():
    initialize_files()
    threading.Thread(target=run_server,daemon=True).start()
    for _ in range(30):
        try: urlopen(API+"/health",timeout=1).close(); break
        except URLError: time.sleep(.2)
    else: raise RuntimeError("API did not start. Check whether port 8765 is already in use.")
    root=tk.Tk()
    def login_screen():
        for w in root.winfo_children(): w.destroy()
        LoginWindow(root,dashboard_screen)
    def dashboard_screen(username):
        for w in root.winfo_children(): w.destroy()
        GymDashboard(root,username,login_screen)
    login_screen(); root.mainloop()
if __name__=="__main__": main()
