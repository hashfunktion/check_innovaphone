#!/usr/bin/env python3
#
# ---------------------------------------------------------------------------------------------------
# check_innovaphone.py
# Icinga check plugin for innovaphone PBX devices.
# 
# Copyright (C) 2019  Jesse Reppin (GitHub @hashfunktion)
#
# Changes:
#   • v1.0 - first release
#
# ---------------------------------------------------------------------------------------------------
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  ---------------------------------------------------------------------------------------------------
#
# Available checks:
#  - Temprature of the PBX (°C)
#  - Sync state of the PBX (ISDN Interaface)
#  - If reset required? (true / false)
#  - Remaining time for software rental licenses in days, hours, minutes, seconds
#
# available options for --command: "temp", "sync", "reset-required", "srlicense"
#
# Befor using, change the "xmlpath" in the check plugin to a writable path for you..
# usage for help: ./check_innovaphone.py
# usage: ./check_innovaphone.py -H <ip or hostname> -l <username> -p <password> --command <check> -w <warning threshold> -c <critical threshold>
#

import sys
import argparse
import urllib.request
import base64
import ssl
import math
import xml.etree.ElementTree as ET

## !--> CHANGE THE XML FILE PATH <-- !
# r/w path for xml files
xmlpath = "/home/it/csvimport/"

# nagios return codes
UNKNOWN = 3
OK = 0
WARNING = 1
CRITICAL = 2
usage = 'usage: ./check_innovaphone.py -H <ip or hostname> -l <username> -p <password> --command <check> -w <warning threshold> -c <critical threshold>'

host = ""
command = ""
username = ""
password = ""
warn = ""
crit = ""
result = ""
perf_data = ""
check_exit = ""
ex = ""

def main():
    global host
    global username
    global password
    global command
    global crit
    global warn
    global result
    global check_exit
    global ex

    result = None

    parser = argparse.ArgumentParser(description='Copyright (C) 2019  Jesse Reppin (GitHub @hashfunktion) - Icinga check plugin for innovaphone PBX devices.')
    parser.add_argument('-H','--hostname', dest='host', action='store',
                        default='<IP or HOSTNAME>',
                        help='enter IP-Adress or Hostname of the innovaphone PBX')
    parser.add_argument('-l','--loginname', dest='username', action='store',
                        default='admin',
                        help='define username from innovaphone PBX (default: admin)')
    parser.add_argument('-p','--password', dest='password', action='store',
                        default='password',
                        help='define password from innovaphone PBX')
    parser.add_argument('--command', dest='command', action='store',
                        default='<command>',
                        help='define the check_command that should be use (available options: "temp", "sync", "reset-required", "srlicense"')
    parser.add_argument('-w','--warning', dest='warn', action='store',
                        default='<warn>',
                        help='define the warning threshold for: temp=XX(°C), srlicense=XXXXXXX(seconds) only XX without unit')
    parser.add_argument('-c','--critical', dest='crit', action='store',
                        default='<crit>',
                        help='define the critical threshold for: temp=XX(°C), srlicense=XXXXXXX(seconds) only XX without unit')

    args = parser.parse_args()

    host = args.host
    username = args.username
    password = args.password
    warn = int
    warn = args.warn
    crit = int
    crit = args.crit
    ex = sys.exit
    command = args.command

    if args.host is None:
        print('Incorrect usage. Host is mandatory (-h).')
        parser.print_help()

    elif args.command is None:
        print('Incorrect usage. Check is mandatory.')
        parser.print_help()
        sys.exit(UNKNOWN)
 
    elif args.command == "temp":
        temp()
    
    elif args.command == "sync":
        sync()
    
    elif args.command == "reset-required":
        resetreq()
    
    elif args.command == "srlicense":
        srlicense()

    else:
        parser.print_help()
        sys.exit(UNKNOWN)

### define COMMAND functions
## TEMP
def temp():
    global host
    global crit
    global warn
    global command
    global result
    global check_exit
    global ex

    result = None

    tempxml = '/CMD0/box_info.xml'
    tempurl = 'https://'+host+tempxml
    
    ssl.match_hostname = lambda cert, hostname: True
    req = urllib.request.Request(tempurl)

    credentials = ('%s:%s' % (username, password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

    res = urllib.request.urlopen(req)
    res_body = res.read()

    with open(xmlpath+command+host+'.xml', 'wb') as f: 
        f.write(res_body) 
    tree = ET.parse(xmlpath+command+host+'.xml')
    root = tree.getroot()

    for sys in root.iter('sys'):
        systemp = sys.get('temp')

    if systemp > crit :
        result = "Temprature is "+systemp+"°C | Temprature="+systemp+";"+warn+";"+crit
        check_exit = "CRITICAL"
        print(check_exit+' - '+result)
        ex(CRITICAL)

    elif systemp > warn:
        result = "Temprature is "+systemp+"°C | Temprature="+systemp+";"+warn+";"+crit
        check_exit = "WARNING"
        print(check_exit+' - '+result)
        ex(WARNING)
   
    elif systemp < warn: 
        result = "Temprature is "+systemp+"°C | Temprature="+systemp+";"+warn+";"+crit
        check_exit = "OK"
        print(check_exit+' - '+result)
        ex(OK)

    else:
        print("Unknown Error!")
        ex(UNKNOWN)

## Sync
def sync():
    global host
    global crit
    global warn
    global command
    global result
    global check_exit
    global ex

    result = None

    tempxml = '/CMD0/box_info.xml'
    tempurl = 'https://'+host+tempxml
    
    ssl.match_hostname = lambda cert, hostname: True
    req = urllib.request.Request(tempurl)

    credentials = ('%s:%s' % (username, password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

    res = urllib.request.urlopen(req)
    res_body = res.read()

    with open(xmlpath+command+host+'.xml', 'wb') as f: 
        f.write(res_body) 
    tree = ET.parse(xmlpath+command+host+'.xml')
    root = tree.getroot()

    for sys in root.iter('sys'):
        sync = sys.get('sync')

    if sync == "-":
        result = "no sync ("+sync+")"
        check_exit = "CRITICAL"
        print(check_exit+' - '+result)
        ex(CRITICAL)

    elif sync != "BRI*" or "PRI*":
        result = "Sync Interface = "+sync
        check_exit = "OK"
        print(check_exit+' - '+result)
        ex(OK)

    else:
        print("Unknown Error!")
        ex(UNKNOWN)

## reset-required
def resetreq():
    global host
    global crit
    global warn
    global command
    global result
    global check_exit
    global ex

    result = None

    tempxml = '/CMD0/box_info.xml'
    tempurl = 'https://'+host+tempxml
    
    ssl.match_hostname = lambda cert, hostname: True
    req = urllib.request.Request(tempurl)

    credentials = ('%s:%s' % (username, password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

    res = urllib.request.urlopen(req)
    res_body = res.read()

    with open(xmlpath+command+host+'.xml', 'wb') as f: 
        f.write(res_body) 
    tree = ET.parse(xmlpath+command+host+'.xml')
    root = tree.getroot()

    for sys in root.iter('sys'):
        rreset = sys.get('reset-required')

    if rreset != None:
        result = "Reset Required: "+rreset
        check_exit = "WARNING"
        print(check_exit+' - '+result)
        ex(WARNING)

    elif rreset is None:
        result = "No Reset Required"
        check_exit = "OK"
        print(check_exit+' - '+result)
        ex(OK)

    else:
        print("Unknown Error!")
        ex(UNKNOWN)

## license time (software rental)
def srlicense():
    global host
    global crit
    global warn
    global command
    global result
    global check_exit
    global ex

    warn_int = int(warn)
    crit_int = int(crit)
    result = None

    tempxml = '/PBX0/ADMIN/mod_cmd_login.xml'
    tempurl = 'https://'+host+tempxml
    
    ssl.match_hostname = lambda cert, hostname: True
    req = urllib.request.Request(tempurl)

    credentials = ('%s:%s' % (username, password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

    res = urllib.request.urlopen(req)
    res_body = res.read()

    with open(xmlpath+command+host+'.xml', 'wb') as f: 
        f.write(res_body) 
    tree = ET.parse(xmlpath+command+host+'.xml')
    root = tree.getroot()

    for info in root.iter('info'):
        xmlseconds = int(info.get('cmd-lics-time'))
    
    seconds = (xmlseconds % 60)
    minutes = ((xmlseconds / 60) % 60)
    hours = (xmlseconds / (60*60) % 24)
    days = ((xmlseconds / (60*60)) / 24)

    result_seconds = math.trunc(seconds)
    result_minutes = math.trunc(minutes)
    result_hours = math.trunc(hours)
    result_days = math.trunc(days)

    srlicensetime = "%s days, %s hours, %s minutes, %s seconds" %(result_days,result_hours,result_minutes,result_seconds)

    if xmlseconds > warn_int:
        result = "Remaining Time: "+srlicensetime
        check_exit = "OK"
        print(check_exit+' - '+result)
        ex(OK)

    elif xmlseconds < warn_int:
        result = "Remaining Time: "+srlicensetime
        check_exit = "WARNING"
        print(check_exit+' - '+result)
        ex(WARNING)
    
    elif xmlseconds < crit_int:
        result = "Remaining Time: "+srlicensetime
        check_exit = "CRITICAL"
        print(check_exit+' - '+result)
        ex(CRITICAL)

    else:
        print("Unknown Error!")
        ex(UNKNOWN)

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

if __name__ == '__main__':
    main()
    sys.exit(UNKNOWN)


