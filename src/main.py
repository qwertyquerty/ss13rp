import pypresence
import time
import win32gui
import win32process
import psutil

while 1:
    try:
        rp=pypresence.Presence("no touching my id")
        rp.connect()
        break
    except:
        time.sleep(300)



servers = {
    "Goonstation #2": ["Goonstation #2","goonhub"],
    "Goonstation RP #1": ["Goonstation RP #1", "goonhub"],
    "Yogstation 13 [99% LAGFREE!]": ["Yogstation 13", "yogstation"],
    "BeeStation - Newbie Friendly!": ["BeeStation", "ss13"],
    "ss13": ["Unknown Server", "ss13"],
    "Oracle Station | Medium RP": ["Oracle Station", "oraclestation"],
    "Hippie Station": ["Hippie Station", "hippiestation"],
    "/tg/Station Bagil": ["Station Bagil", "tgstation"],
    "/tg/Station Sybil": ["Station Sybil", "tgstation"],
    "[99% FREE LAG] Convict Conclave": ["Convict Conclave", "ss13"]
}

def get_server():

    p = [proc for proc in psutil.process_iter() if proc.name() == "dreamseeker.exe"]
    p=p[0]

    def enum_window_callback(hwnd, pid):
        tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid == current_pid:
            windows.append(hwnd)
            
    windows = []
    win32gui.EnumWindows(enum_window_callback, p.pid)
    window = str([win32gui.GetWindowText(item) for item in windows if ":" in win32gui.GetWindowText(item)][0])
    if not window=="Space Station 13" and not window=="BYOND: Your Game Is Starting":
        for i in servers.keys():
            if window.startswith(i):
                return servers[i]
    else:
        server="ss13"
        return servers[server]

while 1:
    try:
        server = get_server()
        rp.update(state=server[0], large_text=server[0], large_image=server[1])
        time.sleep(15)
    except Exception as e:
        rp.clear()
        time.sleep(5)
