#
# spec file for package SFEhive
#
# includes module(s): hive
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include packagenamemacros.inc

%define srcname hive
%define runuser hive
#use random number by userid tool %define runuserid hive
%define runusergroup other

Name:                    SFEhive
IPS_Package_Name:	 developer/distributed/hive
Summary:                 Hive - A data warehouse system for Hadoop
Group:                   Utility
Version:                 0.9.0
URL:		         http://hive.apache.org
Source:		         http://www.us.apache.org/dist/hive/hive-%{version}/hive-%{version}.tar.gz
Source2:                 hive.xml
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /usr
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           %pnm_requires_java_runtime_default
Requires:           SFEhadoop
Requires:           SFEhbase

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
Hive is a data warehouse system for Hadoop that facilitates easy data
summarization, ad-hoc queries, and the analysis of large datasets
stored in Hadoop compatible file systems. Hive provides a mechanism to
project structure onto this data and query the data using a SQL-like
language called HiveQL. At the same time this language also allows
traditional map/reduce programmers to plug in their custom mappers and
reducers when it is inconvenient or inefficient to express this logic
in HiveQL.

%prep
rm -rf %{srcname}-%{version}
%setup -q -n %{srcname}-%{version}
cp %{SOURCE2} hive.xml

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp hive.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p $RPM_BUILD_ROOT/var/log/hive
mkdir -p $RPM_BUILD_ROOT/var/lib/hive

mkdir -p $RPM_BUILD_ROOT/etc
mv conf $RPM_BUILD_ROOT/etc/hive
mkdir -p $RPM_BUILD_ROOT/usr/share/hive
mv docs examples lib scripts bin LICENSE NOTICE *.txt $RPM_BUILD_ROOT/usr/share/hive
rm $RPM_BUILD_ROOT/usr/share/hive/lib/hbase-0.92.0.jar
mkdir $RPM_BUILD_ROOT/usr/bin
ln -s /usr/share/hive/bin/hive-config.sh $RPM_BUILD_ROOT/usr/bin/hive-config.sh
ln -s /usr/share/hive/bin/hive $RPM_BUILD_ROOT/usr/bin/hive

echo "export HIVE_CONF_DIR=/etc/hive" > $RPM_BUILD_ROOT/usr/share/hive/bin/hive-config.sh-new
cat $RPM_BUILD_ROOT/usr/share/hive/bin/hive-config.sh >> $RPM_BUILD_ROOT/usr/share/hive/bin/hive-config.sh-new
echo "export HIVE_HOME=/usr/share/hive" >> $RPM_BUILD_ROOT/usr/share/hive/bin/hive-config.sh-new
cp $RPM_BUILD_ROOT/usr/share/hive/bin/hive-config.sh-new $RPM_BUILD_ROOT/usr/share/hive/bin/hive-config.sh
rm $RPM_BUILD_ROOT/usr/share/hive/bin/hive-config.sh-new
echo "export JAVA_HOME=/usr/java" >> $RPM_BUILD_ROOT/etc/hive/hive-env.sh
echo "export HIVE_LOG_DIR=/var/log/hive" >> $RPM_BUILD_ROOT/etc/hive/hive-env.sh
echo "export HADOOP_HOME=/usr/share/hadoop" >> $RPM_BUILD_ROOT/etc/hive/hive-env.sh
echo "export HIVE_AUX_JARS_PATH=/usr/share/hbase/hbase-0.94.1.jar" >> $RPM_BUILD_ROOT/etc/hive/hive-env.sh

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Hive Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/hive"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for hive)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/hive %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for hive)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/hive %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c HIVE


%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/hive
%{_datadir}/hive/*

%files root
%defattr (-, root, sys)
/etc/hive/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, hive, other) /var/log/hive
%dir %attr(0755, root, other) /var/lib
%dir %attr(0700, hive, other) /var/lib/hive
%dir %attr(0755, root, sys) /var/svc
%dir %attr(0755, root, sys) /var/svc/manifest
%dir %attr(0755, root, sys) /var/svc/manifest/site
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/hive.xml

%changelog
* Sat Oct 6 2012 - Logan Bruns <logan@gedanken.org>
- updated for hbase 0.94.1 compatibility.
* Mon Jun 25 2012 - Logan Bruns <logan@gedanken.org>
- Fixed a classpath, a minor mistake in the smf and moved out of experimental.
* Sun Jun 24 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
