#
# spec file for package SFEhbase
#
# includes module(s): hbase
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include packagenamemacros.inc

%define srcname hbase
%define runuser hbase
#use random number by userid tool %define runuserid hbase
%define runusergroup other

#set to 1 if patched and requires a rebuild before packaging
%define is_patched 0

Name:                    SFEhbase
IPS_Package_Name:	 developer/distributed/hbase
Summary:                 HBase - The Hadoop database
Group:                   Utility
Version:                 0.94.1
URL:		         http://hbase.apache.org
Source:		         http://www.us.apache.org/dist/hbase/hbase-%{version}/hbase-%{version}.tar.gz
Source2:                 hbase.xml
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /usr
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           %pnm_requires_java_runtime_default
%if %is_patched
BuildRequires: %pnm_buildrequires_java_runtime_default
BuildRequires: SFEmaven
%endif

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
Use HBase when you need random, realtime read/write access to your Big
Data. This project's goal is the hosting of very large tables --
billions of rows X millions of columns -- atop clusters of commodity
hardware. HBase is an open-source, distributed, versioned,
column-oriented store modeled after Google's Bigtable: A Distributed
Storage System for Structured Data by Chang et al. Just as Bigtable
leverages the distributed data storage provided by the Google File
System, HBase provides Bigtable-like capabilities on top of Hadoop and
HDFS.

%prep
rm -rf %{srcname}-%{version}
%setup -q -n %{srcname}-%{version}
cp %{SOURCE2} hbase.xml

%build

%if %is_patched
mvn site install assembly:single -Dmaven.test.skip.exec
cp target/hbase-%{version}.jar .
%endif

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp hbase.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p $RPM_BUILD_ROOT/var/log/hbase
mkdir -p $RPM_BUILD_ROOT/var/lib/hbase

mkdir -p $RPM_BUILD_ROOT/etc
mv conf $RPM_BUILD_ROOT/etc/hbase
mkdir -p $RPM_BUILD_ROOT/usr/share/hbase
mv docs lib bin *.jar *.txt $RPM_BUILD_ROOT/usr/share/hbase
mkdir $RPM_BUILD_ROOT/usr/bin
ln -s /usr/share/hbase/bin/hbase-config.sh $RPM_BUILD_ROOT/usr/bin/hbase-config.sh
ln -s /usr/share/hbase/bin/hbase $RPM_BUILD_ROOT/usr/bin/hbase

echo "export HBASE_CONF_DIR=/etc/hbase" > $RPM_BUILD_ROOT/usr/share/hbase/bin/hbase-config.sh-new
cat $RPM_BUILD_ROOT/usr/share/hbase/bin/hbase-config.sh >> $RPM_BUILD_ROOT/usr/share/hbase/bin/hbase-config.sh-new
echo "export HBASE_HOME=/usr/share/hbase" >> $RPM_BUILD_ROOT/usr/share/hbase/bin/hbase-config.sh-new
cp $RPM_BUILD_ROOT/usr/share/hbase/bin/hbase-config.sh-new $RPM_BUILD_ROOT/usr/share/hbase/bin/hbase-config.sh
rm $RPM_BUILD_ROOT/usr/share/hbase/bin/hbase-config.sh-new
echo "export JAVA_HOME=/usr/java" >> $RPM_BUILD_ROOT/etc/hbase/hbase-env.sh
echo "export HBASE_LOG_DIR=/var/log/hbase" >> $RPM_BUILD_ROOT/etc/hbase/hbase-env.sh
echo "export HBASE_MANAGES_ZK=true" >> $RPM_BUILD_ROOT/etc/hbase/hbase-env.sh
echo "export HBASE_REGIONSERVERS=/etc/hbase/regionservers" >> $RPM_BUILD_ROOT/etc/hbase/hbase-env.sh

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="HBase Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/hbase"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for hbase)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/hbase %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for hbase)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/hbase %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c HBASE


%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/hbase
%{_datadir}/hbase/*

%files root
%defattr (-, root, sys)
/etc/hbase/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, hbase, other) /var/log/hbase
%dir %attr(0755, root, other) /var/lib
%dir %attr(0700, hbase, other) /var/lib/hbase
%dir %attr(0755, root, sys) /var/svc
%dir %attr(0755, root, sys) /var/svc/manifest
%dir %attr(0755, root, sys) /var/svc/manifest/site
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/hbase.xml

%changelog
* Sat Oct 6 2012 - Logan Bruns <logan@gedanken.org>
- bumped to 0.94.1 and removed a no longer needed patch 
* Mon Jun 25 2012 - Logan Bruns <logan@gedanken.org>
- add patch to fix hive integration and conditional logic for
  rebuilding with patch.
* Mon Jun 18 2012 - Logan Bruns <logan@gedanken.org>
- bumped to 0.94.0
* Sun Jun 10 2012 - Logan Bruns <logan@gedanken.org>
- Increased the startup and shutdown timeouts. It can take longer with
  a lot of data in the cluster.
* Sat May 12 2012 - Logan Bruns <logan@gedanken.org>
- Moved out of experimental and fixed regionservers variable.
* Fri May 11 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
