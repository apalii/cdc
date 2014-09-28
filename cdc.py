#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import telnetlib as t

'''
Duration calls checker
In order to download :  wget --content-disposition http://pastebin.com/download.php?i=4GZPuFda
 
22.09.2014 - Telnet session was added
'''
 
def show_sip_envs():
    print('Available sip envs :\n')
    with open('/usr/local/etc/active_sipenvs.conf') as file:
        for sipenv in file:
            print sipenv.rstrip()
 
def duration_checker(host, duration=600):
 
    uptime,call_id = [],[]
    tn = t.Telnet(host, "5064")
    tn.write("show call list" + "\n")
 
    for i in tn.read_until("OK").split("\n"):
        if re.search('^\S+@\S+',i):
            x = re.findall('uptime=(\d+\.)', i)
            uptime.append(''.join(x)[:-1])
            y = re.findall('(^\S+@\S+)\sid', i)
            call_id.append(''.join(y)[:-1])
 
    tn.write("q" + "\n")
    calls = dict(zip(uptime, call_id))
    for i in calls:
        if int(i) > duration:
            print calls[i]
 
if __name__ == "__main__":
    import sys
    if sys.argv.__len__() <= 2 or sys.argv.__len__() > 3 :
        show_sip_envs()
        print '''\nHow to use :\n python calls.py <sipenv ip> <duration>'''
        print '''Example : python calls.py 123.123.123.123 600'''
    elif sys.argv.__len__() == 3:  # script with 2 parameters
        if not sys.argv[2].isalpha():
            duration_checker(sys.argv[1], int(sys.argv[2]))
        else : print 'Invalid argument!'



