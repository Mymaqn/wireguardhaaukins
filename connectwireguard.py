#Wireguard connection script for haaukins by Zopazz AKA Jens Alexander Nielsen
import subprocess
import sys
import re
path = None
try: 
    path = sys.argv[1]
except:
    print("Usage: sudo python connectWireguard.py /path/to/conf")
    exit(1)
lines = []
try:
    with open(path,"r") as file:
        lines = file.readlines()
except:
    print("file " +  path + " not found")
    exit(1)
try:
    lines.remove("DNS = 1.1.1.1\n")
except:
    print("Can't find DNS = 1.1.1.1. Might have been removed. Trying to connect anyways")
#grab conn_x filename
pathList = path.split('/')
filename = pathList[len(pathList)-1]
confname = filename.split('.')[0]
try:
    with open("/etc/wireguard/"+filename,"w") as file:
        for item in lines:
            file.write(item)
except:
    print("Failed to open file /etc/wireguard/" + filename + ".\n Are you root?")
    exit(1)
hosts = []
for i in range(0,len(lines)):
    x= re.search("# \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",lines[i])
    if x:
        hosts.append(lines[i].strip("# "))
#We need the current setup of the hostfile to make sure we don't just append a bunch of shit to it
currenthost = None
with open("/etc/hosts", "r") as file:
        currenthost = file.readlines()

with open("/etc/hosts", "a") as file:
    for host in hosts:
        if host in currenthost:
            continue
        file.write(host)
#save the old host file if it's not equal to the old host file
newhost = None
with open("/etc/hosts", "r") as file:
    newhost = file.readlines()
    if currenthost != newhost:
        with open("hosts.old","w") as file2:
            for line in currenthost:
                file2.write(line)
#Then connect with wireguard
runWireguard = "wg-quick up "+confname
process = subprocess.Popen(runWireguard.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
