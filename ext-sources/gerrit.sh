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

# If necessary do first time init
if [ ! -d /var/lib/gerrit/bin ]; then
  /usr/java/bin/java -jar /var/lib/gerrit/gerrit.war init --batch --no-auto-start -d /var/lib/gerrit
  if [ ! $? -eq 0 ]; then
    echo "Gerrit initialization failed." 
    exit $SMF_EXIT_ERR 
  fi

  rm -rf /var/lib/gerrit/logs
  ln -s /var/log/gerrit /var/lib/gerrit/logs
fi

export GERRIT_SITE=/var/lib/gerrit
export GERRIT_WAR=/var/lib/gerrit/gerrit.war
export PATH=$PATH:/usr/gnu/bin
export JAVA_OPTS=-Xmx`/usr/bin/svcprop -p process/max_heap $SMF_FMRI`

/var/lib/gerrit/bin/gerrit.sh start
;; 

'stop') 
export GERRIT_SITE=/var/lib/gerrit
export GERRIT_WAR=/var/lib/gerrit/gerrit.war
export PATH=$PATH:/usr/gnu/bin

/var/lib/gerrit/bin/gerrit.sh start
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
