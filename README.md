cdc
===

Duration calls checker - it is a simple script which allows to check some calls with long duration.
Script takes the following parameters :
1) --ip/-i - IP address of the needed sip environment
2) --duration/-d - Max allowed duration of the call
3) --show - shows call id and duration with some actions.
4) --disconnect - !!! It just disconnects the calls if duration exceed !!!
                      /You have additional 5 second to abort it/
5) --debug - writes some additional information to the log file(/home/porta-one/call_monitor.log)

It possible to use cdc.py without parameters in order to see list of the ip addresses of the available sip envs
on the current sip server.

It seems it is rare used stuff, I've made just for practicing.

10.10.2014 - PEP8 fixes
07.10.2014 - logging
01.10.2014 - normal processing of the parameters and disconnecting were added
30.09.2014 - re and dict processing was enhanced a bit
22.09.2014 - Telnet session was added

Examples :

13:00:49 [ET_SYS MR43.0] porta-one@etsys.intra:~
> sudo python2.7 cdc.py --ip 192.168.197.114 -d 60 --debug --disconnect

Will disconnect all calls with duration more then 60 seconds with debuging information. 
