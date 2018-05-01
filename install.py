import time

try:
    import requests
    import getpass
    USER_NAME = getpass.getuser()
    import subprocess


    install_path = 'C:\\Users\\'+USER_NAME+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'

    print("Installing...\n")
    url = "https://github.com/qwertyquerty/ss13rp/raw/master/ss13rp.exe"
    response = requests.get(url, stream=True)
    handle = open(install_path+"ss13rp.exe", "wb")
    dur = 0
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            dur = dur+1
            if dur % 100 == 0:
                print("#", end="")
            handle.write(chunk)
    print("\n")

    handle.close()
    del chunk
    del handle
    del response

    print("Installed!\n")
    print("Starting...\n")
    subprocess.Popen("\""+install_path+"ss13rp.exe\"")
    print("Started!\n")
    time.sleep(1)
except:
    print("Error!")
    time.sleep(1)
