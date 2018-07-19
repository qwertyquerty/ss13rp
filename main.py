import pypresence
import time
import win32gui
import win32process
import psutil
import sys
import util
import requests
import time

if "join" in sys.argv:
    print("joining game...")
    def join(ev):
        print(ev)
    rp = pypresence.Client("440289271580983308")
    rp.start()
    print(rp.read())
    rp.register_event("ACTIVITY_JOIN", join)
    rp.loop.run_forever()

else:

    while True:

        try:
            rp = pypresence.Client("440289271580983308")
            rp.start()
            break
        except:
            time.sleep(60)


    servers = {
        "Goonstation #2": ["Goonstation #2", "goonhub", "goon2.goonhub.com", 26200, "fetch"],
        "Goonstation RP #1": ["Goonstation RP #1", "goonhub", "goon1.goonhub.com", 26100, "fetch"],
        "Yogstation 13 [99% LAGFREE!]": ["Yogstation 13", "yogstation"],
        "BeeStation 13": ["BeeStation", "beestation", "198.58.107.171", 3333, "fetch"],
        "ss13": ["Unknown Server", "ss13"],
        "Oracle Station | Medium RP": ["Oracle Station", "oraclestation"], #"byond.oraclestation.com", 5000
        "Hippie Station": ["Hippie Station", "hippiestation"],
        "/tg/Station Bagil": ["Station Bagil", "tgstation", "bagil.aws.tgstation13.org", 2337, "fetch"],
        "/tg/Station Sybil": ["Station Sybil", "tgstation", "sybil.aws.tgstation13.org", 1337, "fetch"],
        "/tg/Station Terry": ["Station Terry", "tgstation", "terry.tgstation13.org", 3337, "fetch"],
        "[99% FREE LAG] Convict Conclave": ["Convict Conclave", "ss13"],
        "[ss13.ru] Yellow Circus": ["Yellow Circus", "ss13"],
        "Persistence Station 13": ["Persistence Station", "persistence"],
        "Apollo Gaming": ["Apollo Gaming","apollo"],
        "Lebensraum Alpha": ["Lebensraum Alpha", "ss13"],
        "Baystation 12": ["Baystation 12", "bs12", "play.baystation12.net", 8000, "fetch"],
        "FTL13": ["FTL13", "ftl13", "ftl13.com", 7777, "fetch"],
        "Tool Box Station": ["Toolbox Station", "toolbox"],
        "Pressurized Roleplay": ["Pressurized Roleplay", "pressure"],
        "StarTrek13": ["Star Trek 13", "startrek"],
        "Polaris Station 13": ["Polaris Station", "polaris"],
        "Paradise Station 13": ["Paradise Station", "paradise"],
        "Aurora Station": ["Aurora Station", "ss13"],
        "VOREStation": ["VOREStation", "citadel", "citadel-station.net", 44150, "fetch"],
        "Citadel Station 13": ["Citadel Station", "citadel", "citadel-station.net", 44130, "fetch"],
        "Colonial Marines": ["Colonial Marines", "cm"]
    }


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

        p = [proc for proc in psutil.process_iter() if proc.name() ==
             "dreamseeker.exe"]

        p = p[0]

        windows=get_hwnds_for_pid(p.pid)


        windowtitles = [i for i in [str(win32gui.GetWindowText(item))
                      for item in windows] if i != ""]
        print(windowtitles)

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
            print(server)
            if len(server) == 5:
                try:
                    if server[4] == "fetch":
                        status = util.fetch(server[2], server[3], "status")
                    elif server[4] == "http":
                        status = requests.get(server[2]).json()
                    #print(status)
                    if server[0] in ["Baystation 12"]:
                        details = status["map"]+" | "+str(status["players"])+" players"
                    elif server[0] in ["Goonstation #2","Goonstation RP #1", "BeeStation", "FTL13", "Station Bagil", "Station Terry", "Station Sybil", "Citadel Station"]:
                        details = status["map_name"]+" | "+str(status["players"])+" players"

                    if server[0] in ["Goonstation #2","Goonstation RP #1"]:
                        if status["shuttle_time"] != 'welp' and status["shuttle_time"] != '600':
                            rp.set_activity(state=server[0],details=details,large_text=server[0],large_image=server[1], start=int(time.time())-int(status["elapsed"]), end=int(time.time())+int(status["shuttle_time"]))
                        else:
                            rp.set_activity(state=server[0],details=details,large_text=server[0],large_image=server[1], start=int(time.time())-int(status["elapsed"]))

                    elif server[0] in ["BeeStation", "FTL13", "Station Bagil", "Station Terry", "Station Sybil", "Citadel Station"]:
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
            try:
                rp.clear_activity()
                time.sleep(5)
            except Exception as e:
                print(e)
                while True:
                    try:
                        rp = pypresence.Client("440289271580983308")
                        rp.start()
                        break
                    except:
                        time.sleep(30)
