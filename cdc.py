#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Call monitor
*python 2.7 or higher is required'''
import re
import telnetlib as t
import time
import logging
import os.path

logger = logging.getLogger(__name__)
try:
    handler = logging.FileHandler('/home/porta-one/call_monitor.log')
except IOError as e:
    print "({})".format(e)
formatter = logging.Formatter(u'%(asctime)s [LINE:%(lineno)d] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def show_sip_envs():
    ''' Shows sipenvs'''
    sipenvs = '/usr/local/etc/active_sipenvs.conf'
    if os.path.isfile(sipenvs):
        with open(sipenvs) as active_sipenvs_conf:
            for sipenv in active_sipenvs_conf:
                print sipenv.rstrip()
    else:
        logger.debug('Can not find %s', sipenvs)


def duration_checker(host, duration=600):
    '''Parse and collect uptime and call ids'''
    uptime_list, call_id_list = [], []
    try:
        telnet = t.Telnet(host, "5064")
        telnet.write("show call list" + "\n")
        for i in telnet.read_until("OK").split("\n"):
            if re.search('^\S+@\S+', i):
                uptime = re.findall('uptime=(\d+)', i)
                if int(uptime[0]) > duration:
                    uptime_list.append(''.join(uptime))
                    call_id = re.findall('(^\S+@\S+):', i)
                    call_id_list.append(''.join(call_id))
        calls = dict(zip(uptime_list, call_id_list))
        logger.debug('Connection with [%s] is established', host)
    except IOError as e:
        print "({})".format(e)
        logger.debug('Connection with [%s] is not established', host)

    for i in calls:
        if args.show is True:
            print '{call_id} : {duration}'.format(duration=i, call_id=calls[i])
            time.sleep(0.1)
        else:
            print calls[i]

    if args.disconnect:
        print '\nCalls will be disconnected in 5 seconds ! \
        You can press ctrl+C to abort.'
        time.sleep(5)
        for i in calls.values():
            telnet.write("disconnect " + i + "\n")
            logger.debug('Call %s was disconnected', i)

    telnet.write("q" + "\n")
    logger.debug('Telnet connection to %s is closed', host)

if __name__ == "__main__":
    import sys
    import argparse
    if len(sys.argv) == 1:
        show_sip_envs()
    else:
        parser = argparse.ArgumentParser(description='Call Monitor v.2')
        parser.add_argument("--ip", "-i", type=str,
                            help="Ip address of the sip env")
        parser.add_argument("--duration", "-d", type=int, default=600)
        parser.add_argument("--show", action='store_true',
                            help="Shows call_id and duration")
        parser.add_argument("--disconnect", action='store_true',
                            help="This option will disconnect the calls.")
        parser.add_argument("--debug", action='store_true', help="Debug")
        args = parser.parse_args()
        if args.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        if args.ip is None:
            print 'IP address of the sipenv is required !'
            sys.exit(0)
        else:
            duration_checker(args.ip, args.duration)
