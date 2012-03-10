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
/usr/java/bin/java -jar /var/lib/jenkins/jenkins.war \
  --httpPort=`/usr/bin/svcprop -p listener/http_port $SMF_FMRI` \
  --httpListenAddress=`/usr/bin/svcprop -p listener/http_address $SMF_FMRI` \
  --ajp13Port=`/usr/bin/svcprop -p listener/ajp_port $SMF_FMRI` \
  2>/var/log/jenkins/jenkins.log &
echo $! > /var/lib/jenkins/jenkins.pid
;; 

'stop') 
if [ -f /var/lib/jenkins/jenkins.pid ]; then
    kill `cat /var/lib/jenkins/jenkins.pid`
    rm /var/lib/jenkins/jenkins.pid
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
