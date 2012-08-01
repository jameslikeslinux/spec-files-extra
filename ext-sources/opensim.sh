#!/bin/bash

. /lib/svc/share/smf_include.sh

getproparg() { 
val=`svcprop -p $1 $SMF_FMRI` 
[ -n "$val" ] && echo $val 
} 

if [ -z "$SMF_FMRI" ]; then 
echo "SMF framework variables are not initialized." 
exit $SMF_EXIT_ERR 
fi

case "$1" in 
'start') 
# ugly hack to work around not be able to use spaces in ips packages
find /var/lib/opensim -name "*^*" -print | awk '{printf "mv \"%s\" \"`echo %s | tr ^ \\ `\"\n", $0, $0}' | bash

/usr/mono/bin/mono /var/lib/opensim/OpenSim.exe \
  2>>/var/log/opensim/opensim.log &
echo $! > /var/lib/opensim/opensim.pid
;; 

'stop') 
if [ -f /var/lib/opensim/opensim.pid ]; then
    kill `cat /var/lib/opensim/opensim.pid`
    rm /var/lib/opensim/opensim.pid
fi
;; 

'refresh') 
echo "not implemented"
;; 

*) 
echo $"Usage: $0 {start|refresh}" 
exit 1 
;; 

esac 
exit $SMF_EXIT_OK
