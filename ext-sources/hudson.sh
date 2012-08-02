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
/usr/java/bin/java -jar /var/lib/hudson/hudson.war \
  --httpPort=`/usr/bin/svcprop -p listener/http_port $SMF_FMRI` \
  2>/var/log/hudson/hudson.log &
echo $! > /var/lib/hudson/hudson.pid
;; 

'stop') 
if [ -f /var/lib/hudson/hudson.pid ]; then
    kill `cat /var/lib/hudson/hudson.pid`
    rm /var/lib/hudson/hudson.pid
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
