#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import telnetlib as t
import time

'''
Call monitor 
*python 2.7 or higher is required

01.10.2014 - normal processing of the parameters and disconnecting were added
30.09.2014 - re and dict processing was enhanced a bit
22.09.2014 - Telnet session was added
'''
 
def show_sip_envs():
    with open('/usr/local/etc/active_sipenvs.conf') as file:
        for sipenv in file:
            print sipenv.rstrip()
 
def duration_checker(host, duration=600):
    uptime,call_id = [],[]
    tn = t.Telnet(host, "5064")
    tn.write("show call list" + "\n")
 
    for i in tn.read_until("OK").split("\n"):
        if re.search('^\S+@\S+',i):
            x = re.findall(r'uptime=(\d+)', i)
            if int(x[0]) > duration :
                uptime.append(''.join(x))
                y = re.findall(r'(^\S+@\S+):', i)
                call_id.append(''.join(y))
    calls = dict(zip(uptime, call_id))

    for i in calls:
        if args.show is True:
            print '{call_id} : {duration}'.format(duration=i, call_id=calls[i])
            time.sleep(0.1)
        else : 
            print calls[i]

    if args.disconnect:
        print '\nCalls will be disconnected in 5 seconds ! You can press ctrl+C to abort.'
        time.sleep(5)
        for i in calls.values():
            tn.write("disconnect " + i + "\n")

    tn.write("q" + "\n")
    print 'Telnet connection closed' 

if __name__ == "__main__":
    import sys
    import argparse
    if len(sys.argv) == 1 :
        show_sip_envs()
    else:
        p = argparse.ArgumentParser(description='Call Monitor v.2')
        p.add_argument("--ip","-i", type=str, help="Ip address of the sip env")
        p.add_argument("--duration","-d",type=int, default=600, help="Max. duration of the call")
        p.add_argument("--show", action='store_true', help="It will show call_id and duration")
        p.add_argument("--disconnect", action='store_true', help="This option will disconnect the calls. Be careful!")
        args = p.parse_args()
        if args.ip is None : 
            print 'IP address of the sipenv is required !'
            sys.exit(0)
        else:
            duration_checker(args.ip, args.duration)