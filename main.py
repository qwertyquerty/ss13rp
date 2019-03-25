import pypresence
import time
import win32gui
import win32process
import psutil
import sys
import util
import requests
import time
from config import *
import webbrowser

if "join" in sys.argv:
	print("joining game...")
	def join(ev):
		ie = webbrowser.get(webbrowser.BackgroundBrowser)
		ie.open('') #py 3.6 breaks this
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
			time.sleep(15)

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
			activity = {"large_text": server[0], "large_image":server[1]}
			if len(server) >= 5:
				try:
					if server[4] == "fetch":
						status = util.fetch(server[2], server[3], "status")
						print("Status (fetch): "+str(status))
					elif server[4] == "http":
						status = requests.get(server[2]).json()
						print("Status (http): "+str(status))

					if server[0] in ["Bagil Station", "Terry Station", "Sybil Station", "Citadel Station", "FTL13"]:
						activity["start"] = int(time.time())-int(status["round_duration"])
						activity["party_id"] = str(status["round_id"]) + " | " + status["map_name"] #apparently terry has NO revision
						#activity["join"] = party id + server name
						#activity["spectate"] = party id + server name

						if status["round_id"]: #check if round id is avalable
							activity["details"] = "Map: "+status["map_name"]+" | Gamemode: "+status["mode"]+" | Round id: "+str(status["round_id"])
						else:
							activity["details"] = "Map: "+status["map_name"]+" | Gamemode: "+status["mode"]

						if status["popcap"]: #fetch popcap
							activity["party_size"] = [int(status["players"])] + [int(status["popcap"])]
						else: #best guess maxcap
							activity["party_size"] = [int(status["players"])] + [90]

						actualstatus = int(status["gamestate"])
						if actualstatus == 0: #0: init, 1:lobbywait 2:start
							activity["state"] = "Initializing game"
							activity["instance"] = False
						elif actualstatus == 1:
							activity["state"] = "Waiting on Lobby"
							activity["instance"] = True
						elif actualstatus == 2:
							activity["state"] = "Starting"
						elif actualstatus == 3:
							activity["state"] = "Started"
						elif actualstatus == 4:
							activity["state"] = "Round ended!"
							activity["instance"] = False

					if server[0] in ["Baystation 12"]:
						activity["details"] = "Map: "+status["map"]+" | Players"+str(status["players"])
					elif server[0] in ["Goonstation #2","Goonstation RP #1", "Hippie Station", "BeeStation", "Yogstation 13"]:
						activity["details"] = "Map: "+status["map_name"]+" | Players"+str(status["players"])
					elif server[0] in ["VOREStation"]: #apparently this fucker dosen't return map data
						activity["details"] = "Gamemode: "+status["mode"]+" | Players"+status["players"]

					if server[0] in ["Goonstation #2","Goonstation RP #1"]:
						activity["start"] = int(time.time())-int(status["elapsed"])
					elif server[0] in ["Hippie Station", "BeeStation", "Yogstation 13"]:
						activity["start"] = int(time.time())-int(status["round_duration"])
					elif server[0] in ["VOREStation"]: #andd also it fucking returns time (in string) not in VARS!
						ittimetostop = status["roundduration"]
						ittimetostop = ittimetostop.split(':')
						activity["start"] = int(time.time())-(int(ittimetostop[0]) + int(ittimetostop[1]))

				except Exception as E:
					print(E)
					pass

			rp.set_activity(**activity)
			print(str(activity))
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