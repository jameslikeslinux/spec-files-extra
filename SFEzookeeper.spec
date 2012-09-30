#
# spec file for package SFEzookeeper
#
# includes module(s): zookeeper
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include packagenamemacros.inc

%define srcname zookeeper
%define runuser zkuser
#use random number by userid tool %define runuserid zkuser
%define runusergroup other

Name:                    SFEzookeeper
IPS_Package_Name:	 developer/distributed/zookeeper
Summary:                 ZooKeeper - coordinating distributed systems
Group:                   Utility
Version:                 3.4.4
URL:		         http://zookeeper.apache.org
Source:		         http://www.us.apache.org/dist/zookeeper/zookeeper-%{version}/zookeeper-%{version}.tar.gz
Source2:                 zookeeper.xml
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /usr
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           %pnm_requires_java_runtime_default

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
ZooKeeper is a centralized service for maintaining configuration
information, naming, providing distributed synchronization, and
providing group services. All of these kinds of services are used in
some form or another by distributed applications. Each time they are
implemented there is a lot of work that goes into fixing the bugs and
race conditions that are inevitable. Because of the difficulty of
implementing these kinds of services, applications initially usually
skimp on them ,which make them brittle in the presence of change and
difficult to manage. Even when done correctly, different
implementations of these services lead to management complexity when
the applications are deployed.

%prep
rm -rf %{srcname}-%{version}
%setup -q -n %{srcname}-%{version}
cp %{SOURCE2} zookeeper.xml

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp zookeeper.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p $RPM_BUILD_ROOT/var/log/zookeeper
mkdir -p $RPM_BUILD_ROOT/var/lib/zookeeper

mkdir -p $RPM_BUILD_ROOT/etc
mv conf $RPM_BUILD_ROOT/etc/zookeeper
sed 's|/tmp/zookeeper|/var/lib/zookeeper|g' $RPM_BUILD_ROOT/etc/zookeeper/zoo_sample.cfg > $RPM_BUILD_ROOT/etc/zookeeper/zoo.cfg
mkdir -p $RPM_BUILD_ROOT/usr/share/zookeeper
mv docs lib *.jar *.txt $RPM_BUILD_ROOT/usr/share/zookeeper
mkdir -p $RPM_BUILD_ROOT/usr/share/zookeeper/bin
for f in bin/*.sh ; do
  sed -e 's|/bin/sh|/bin/bash|g' \
      -e 's|grep|ggrep|g' \
      -e 's|ZOOBINDIR=`cd ${ZOOBIN}; pwd`|ZOOBINDIR=/usr/share/zookeeper/bin|g' \
      -e 's|ZOOCFGDIR="$ZOOBINDIR/../etc/zookeeper"|ZOOCFGDIR=/etc/zookeeper|g' \
      $f > $RPM_BUILD_ROOT/usr/share/zookeeper/$f
  chmod a+x $RPM_BUILD_ROOT/usr/share/zookeeper/$f
done

mkdir $RPM_BUILD_ROOT/usr/bin
ln -s /usr/share/zookeeper/bin/zkCli.sh $RPM_BUILD_ROOT/usr/bin/zookeeper

echo "export JAVA_HOME=/usr/java" > $RPM_BUILD_ROOT/etc/zookeeper/zookeeper-env.sh
echo "export ZOO_LOG_DIR=/var/log/zookeeper" >> $RPM_BUILD_ROOT/etc/zookeeper/zookeeper-env.sh

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Zookeeper Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/zookeeper"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for zookeeper)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/zookeeper %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for zookeeper)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/zookeeper %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c ZOOKEEPER


%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/zookeeper
%{_datadir}/zookeeper/*

%files root
%defattr (-, root, sys)
/etc/zookeeper/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, %{runuser}, other) /var/log/zookeeper
%dir %attr(0755, root, other) /var/lib
%dir %attr(0700, %{runuser}, other) /var/lib/zookeeper
%dir %attr(0755, root, sys) /var/svc
%dir %attr(0755, root, sys) /var/svc/manifest
%dir %attr(0755, root, sys) /var/svc/manifest/site
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/zookeeper.xml

%changelog
* Sun Sep 30 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
