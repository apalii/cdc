hcc*
===

Hunged calls checker - it is a simple script which allows to check some calls with exceeded duration.
Script takes the following parameters :
1) --ip/-i - IP address of the needed sip environment
2) --duration/-d - Max allowed duration of the call
3) --show - shows call id and duration with some actions.
4) --disconnect - !!! It just disconnects the calls if duration exceed !!!
                      /You have additional 5 second to abort it/
5) --debug - writes some additional information to the log file(/home/porta-one/call_monitor.log)

It possible to use hcc.py without parameters in order to see list of the ip addresses of the available sip envs
on the current sip server.

*It seems it is rare used stuff, I've it made just for practicing.

26.10.2014 - added previous ability to specify --ip and --duration
             if ip or durations was missed script will catch it
             some improvements with reading files
23.10.2014 - getting durations from the config files, renamed to the hcc
10.10.2014 - PEP8 fixes
07.10.2014 - logging
01.10.2014 - normal processing of the parameters and disconnecting were added
30.09.2014 - re and dict processing was enhanced a bit
22.09.2014 - Telnet session was added

Examples :

> sudo python2.7 hcc.py
-will show all sip envs on the current server

> sudo python2.7 hcc.py --ip 192.168.197.114 -d 600 --debug --disconnect
-will disconnect all calls with duration more then 60 seconds with debuging information. 

> sudo python2.7 hcc.py --debug --show
- will show all (possible)hunged calls for every sip env

> How to download script on the particular server ?
wget --no-check-certificate --content-disposition https://raw.githubusercontent.com/apalii/hcc/master/hcc.py
