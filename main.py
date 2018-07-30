import pypresence
import time
import win32gui
import win32process
import psutil
import sys
import util
import requests
import time
import json
from config import *

if "join" in sys.argv:
    print("joining game...")
    def join(ev):
        print(ev)
    rp = pypresence.Client(client_id)
    rp.start()
    print(rp.read())
    rp.register_event("ACTIVITY_JOIN", join)
    rp.loop.run_forever()

else:

    while True:
        try:
            rp = pypresence.Client(client_id)
            rp.start()
            break
        except:
            time.sleep(20)





    def get_hwnds_for_pid (pid):
      def callback (hwnd, hwnds):
        if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
          _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
          if found_pid == pid:
            hwnds.append (hwnd)
        return True

      hwnds = []
      win32gui.EnumWindows (callback, hwnds)
      return hwnds



    def get_server():

        p = [proc for proc in psutil.process_iter() if proc.name() == "dreamseeker.exe"]

        p = p[0]

        windows=get_hwnds_for_pid(p.pid)


        windowtitles = [i for i in [str(win32gui.GetWindowText(item))
                      for item in windows] if i != ""]


        for title in windowtitles:
            if not title == "Space Station 13":
                for i in servers.keys():
                    if title.startswith(i):

                        return servers[i]

            else:
                server = "ss13"
                return servers[server]


    while True:
        try:
            server = get_server()

            if len(server) == 5:
                try:

                    if server[4] == "fetch":
                        status = util.fetch(server[2], server[3], "status")
                    elif server[4] == "http":
                        status = json.loads(requests.get(server[2]).content.decode('utf-8', 'ignore').strip().split("?status\x00")[1])

                    if server[0] in ["Baystation 12"]:
                        details = status["map"]+" | "+str(status["players"])+" players"

                    elif server[0] in ["Goonstation #2","Goonstation RP #1", "Hippie Station", "BeeStation", "FTL13", "Station Bagil", "Station Terry", "Station Sybil", "Citadel Station", "Yogstation 13"]:
                        details = status["map_name"]+" | "+str(status["players"])+" players"
                    if server[0] in ["Goonstation #2","Goonstation RP #1"]:
                        rp.set_activity(state=server[0],details=details,large_text=server[0],large_image=server[1], start=int(time.time())-int(status["elapsed"]))
                    elif server[0] in ["Hippie Station", "BeeStation", "FTL13", "Station Bagil", "Station Terry", "Station Sybil", "Citadel Station", "Yogstation 13"]:
                        rp.set_activity(state=server[0],details=details,large_text=server[0],large_image=server[1], start=int(time.time())-int(status["round_duration"]))


                    else:
                        rp.set_activity(state=server[0],details=details,large_text=server[0],large_image=server[1])


                except Exception as E:
                    print(E)
                    rp.set_activity(state=server[0],large_text=server[0],large_image=server[1])
            else:
                rp.set_activity(state=server[0],large_text=server[0],large_image=server[1])

            time.sleep(15)

        except Exception as e:
            print(e)
            time.sleep(10)
            try:
                rp.clear_activity()
                time.sleep(5)
            except Exception as e:
                print(e)
                while True:
                    try:
                        rp = pypresence.Client(client_id)
                        rp.start()
                        break
                    except:
                        time.sleep(20)
