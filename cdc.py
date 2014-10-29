#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Hung call checker v.4
*python 2.7 or higher is required'''
import re
import telnetlib as t
import time
import logging
import os.path
import sys
import argparse

parser = argparse.ArgumentParser(description='Hung call checker v.3')
parser.add_argument("--ip", "-i", type=str,
                    help="Ip address of the sip env")
parser.add_argument("--duration", "-d", type=int)
parser.add_argument("--show", action='store_true',
                    help="Shows call_id and duration")
parser.add_argument("--disconnect", action='store_true',
                    help="This option will disconnect the calls.")
parser.add_argument("--debug", action='store_true', help="Debug")
args = parser.parse_args()

logger = logging.getLogger(__name__)
try:
    handler = logging.FileHandler('/home/porta-one/call_monitor.log')
except IOError as e:
    print '( {} )'.format(e)
    sys.exit(0)
formatter = logging.Formatter(u'%(asctime)s [LINE:%(lineno)d] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
if args.debug:
    logger.setLevel(logging.DEBUG)
    logger.debug('-' * 40)
    logger.debug(args)
else:
    logger.setLevel(logging.INFO)

def show_sip_envs():
    ''' Shows sipenvs'''
    sipenvs = '/usr/local/etc/active_sipenvs.conf'
    if os.path.isfile(sipenvs):
        with open(sipenvs) as active_sipenvs_conf:
            for sipenv in active_sipenvs_conf:
                print sipenv.rstrip()
    else:
        logger.debug('Can not find %s', sipenvs)
        sys.exit(0)


def get_durations(): 
    '''Return dict with ips of the sip envs as keys and 
    max_credit_time value as values '''
    sipenvs = '/usr/local/etc/active_sipenvs.conf'
    conf_paths = []
    durations = [] 
    ips = []
    if os.path.isfile(sipenvs):
        with open(sipenvs) as active_sipenvs_conf:
            for ip in active_sipenvs_conf:
                conf_paths.append('/porta_var/sipenv-' + ip.rstrip() + '/etc/b2bua.conf')
                ips.append(ip.rstrip())
    else:
        logger.debug('%s file not found', sipenvs)
        sys.exit(0)
    for config in conf_paths:
        with open(config) as config_file:
            for line in config_file:
                if line.startswith('max_credit_time'):
                    durations.append(line.rstrip()[16:])
                    break
    ips_durations = dict(zip(ips, durations))
    return ips_durations 


def duration_checker(host, duration=14440):
    '''Collect uptime and call_ids'''
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
        logger.debug('Connection to [%s] is established', host)
    except IOError as e:
        print '( {} )'.format(e)
        logger.debug('Connection to [%s] is not established', host)
        sys.exit(0)

    print "SIP {} | Analyzing calls ...".format(host)
    time.sleep(1)
    if len(calls) == 0:
        print "There are no calls which exceed the specified duration"
    else:     
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
    if len(sys.argv) == 1:
        show_sip_envs()
    else:
        if args.ip is None and args.duration is None :
            for ip, dur in get_durations().items():
                duration_checker(ip, dur)
        if (args.ip is None and args.duration is not None) or \
           (args.ip is not None and args.duration is None):
            print "ip or duration is missing !\nUse --help"
        if args.ip is not None and args.duration is not None:
            duration_checker(args.ip, args.duration)
<<<<<<< HEAD
=======
            
>>>>>>> 6dfb27803445a992a99b70b05ab4881ab54ebcfe
