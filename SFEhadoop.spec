#
# spec file for package SFEhadoop
#
# includes module(s): hadoop
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%define srcname hadoop
%define runuser hadoop
#use random number by userid tool %define runuserid hadoop
%define runusergroup other

Name:                    SFEhadoop
IPS_Package_Name:	 developer/distributed/hadoop
Summary:                 Hadoop - Open-source software for reliable, scalable, distributed computing.
Group:                   Utility
Version:                 1.0.3
URL:		         http://hadoop.apache.org
Source:		         http://www.us.apache.org/dist/hadoop/core/hadoop-%{version}/hadoop-%{version}.tar.gz
Source2:                 hadoop.xml
Patch1:        	         hadoop-01-task-controller-make.diff
Patch2:                  hadoop-02-skip-jsvc.diff
Patch3:                  hadoop-03-fix-file-flags.diff
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /usr
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:      developer/build/ant
BuildRequires:      SFEgcc
Requires:           SFEgccruntime
Requires:           %pnm_requires_java_runtime_default
Requires:           SFEsnappy

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
The Apache Hadoop software library is a framework that allows for the
distributed processing of large data sets across clusters of computers
using a simple programming model. It is designed to scale up from
single servers to thousands of machines, each offering local
computation and storage. Rather than rely on hardware to deliver
high-avaiability, the library itself is designed to detect and handle
failures at the application layer, so delivering a highly-availabile
service on top of a cluster of computers, each of which may be prone
to failures.

%prep
rm -rf %{srcname}-%{version}
%setup -q -n %{srcname}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
chmod a+x src/*.sh
cp %{SOURCE2} hadoop.xml

%build

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -D_POSIX_PTHREAD_SEMANTICS"
#export LDFLAGS="%_ldflags"
export LDFLAGS="-L/usr/jdk/latest/jre/lib/i386/"
export JAVA_HOME=/usr/java
ant -Dcompile.native=true -Dversion=%{version} compile
mkdir lib/native/SunOS-x86-32
cp build/native/SunOS-x86-32/.libs/libhadoop* lib/native/SunOS-x86-32
ant -Dversion=%{version} bin-package

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/lib/
mv build/native/SunOS-x86-32/.libs/libhadoop* $RPM_BUILD_ROOT/usr/lib/
rm $RPM_BUILD_ROOT/usr/lib/libhadoop.la*

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp hadoop.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p $RPM_BUILD_ROOT/var/log/hadoop
mkdir -p $RPM_BUILD_ROOT/var/lib/hadoop

cd build/hadoop-%{version}
mv bin/task-controller sbin
mv etc $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
mv share $RPM_BUILD_ROOT/usr
mv bin sbin libexec $RPM_BUILD_ROOT/usr/share/hadoop
mkdir $RPM_BUILD_ROOT/usr/bin
ln -s /usr/share/hadoop/libexec/hadoop-config.sh $RPM_BUILD_ROOT/usr/bin/hadoop-config.sh
ln -s /usr/share/hadoop/bin/hadoop $RPM_BUILD_ROOT/usr/bin/hadoop

echo "export HADOOP_CONF_DIR=/etc/hadoop" > $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new
cat $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh >> $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new
echo "export HADOOP_HOME=/usr/share/hadoop" >> $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new
cp $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh
rm $RPM_BUILD_ROOT/usr/share/hadoop/libexec/hadoop-config.sh-new
echo "export JAVA_HOME=/usr/java" >> $RPM_BUILD_ROOT/etc/hadoop/hadoop-env.sh
echo "export HADOOP_LOG_DIR=/var/log/hadoop" >> $RPM_BUILD_ROOT/etc/hadoop/hadoop-env.sh

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Hadoop Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/hadoop"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for hadoop)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/hadoop %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for hadoop)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/hadoop %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c HADOOP


%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/hadoop
%{_datadir}/hadoop/*
%dir %attr(0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, other) %{_datadir}/doc/hadoop
%{_datadir}/doc/hadoop/*

%files root
%defattr (-, root, sys)
/etc/hadoop/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, hadoop, other) /var/log/hadoop
%dir %attr(0755, root, other) /var/lib
%dir %attr(0700, hadoop, other) /var/lib/hadoop
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/hadoop.xml

%changelog
* Mon Jun 18 2012 - Logan Bruns <logan@gedanken.org>
- bumped to 1.0.3
* Sun Jun 10 2012 - Logan Bruns <logan@gedanken.org>
- Increased the startup and shutdown timeouts. It can take longer with
  a lot of data in the cluster.
* Thu May 3 2012 - Logan Bruns <logan@gedanken.org>
- Replaced linux file flags with solaris ones
* Sat Apr 28 2012 - Logan Bruns <logan@gedanken.org>
- Added snappy to requires (really optional)
- Put home directory back to hold ssh keys
- Moved out of experimental
* Fri Apr 27 2012 - Logan Bruns <logan@gedanken.org>
- Fixes for building native task-controller, better directory usage and such.
* Wed Apr 25 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
