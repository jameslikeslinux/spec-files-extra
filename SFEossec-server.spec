#
# spec file for package SFEossec-server
#
# includes module(s): ossec-server
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define _basedir /var

%define srcname ossec-hids

Name:                    SFEossec-server
IPS_Package_Name:	 security/ossec-server
Summary:                 OSSEC - open source Host-based Intrusion Detection System (HIDS)
Group:                   Applications/System Utilities
Version:                 2.5.1
URL:		         http://www.ossec.net
Source:		         http://www.ossec.net/files/%srcname-%version.tar.gz
Source2:                 ossec.xml
License: 		 GPLv2
Patch1:                  ossec-server-01-installserver.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:      SFEgcc
Requires:           SFEgccruntime

Requires: %name-root
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
Requires:	%name

%description
OSSEC is a scalable, multi-platform, open source Host-based Intrusion
Detection System (HIDS). It has a powerful correlation and analysis
engine, integrating log analysis, file integrity checking, Windows
registry monitoring, centralized policy enforcement, rootkit
detection, real-time alerting and active response.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
%patch1 -p1

#ossec manifest
cp -p %{SOURCE2} ossec.xml

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

cd src
make -j$CPUS all
make -j$CPUS build

%install
rm -rf $RPM_BUILD_ROOT

cd src
mv LOCATION LOCATION.orig
sed s^/var/ossec^$RPM_BUILD_ROOT/var/ossec^ < LOCATION.orig > LOCATION
make -j$CPUS server

# Generate the /etc/ossec-init.conf
VERSION_FILE="./VERSION"
VERSION=`cat ${VERSION_FILE}`
OSSEC_INIT=$RPM_BUILD_ROOT/var/ossec/etc/ossec-init.conf
echo "DIRECTORY=\"/var/ossec\"" > ${OSSEC_INIT}
echo "VERSION=\"${VERSION}\"" >> ${OSSEC_INIT}
echo "DATE=\"`date`\"" >> ${OSSEC_INIT}
echo "TYPE=\"server\"" >> ${OSSEC_INIT}

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp ../ossec.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/groupadd ossec';
  echo '/usr/sbin/useradd -d /var/ossec -s /bin/true -g ossec ossec';
  echo '/usr/sbin/useradd -d /var/ossec -s /bin/true -g ossec ossecm';
  echo '/usr/sbin/useradd -d /var/ossec -s /bin/true -g ossec ossecr';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel ossec';
  echo '/usr/sbin/userdel ossecm';
  echo '/usr/sbin/userdel ossecr';
  echo '/usr/sbin/groupdel ossec';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions
group groupname="ossec"
user ftpuser=false gcos-field="OSSEC Reserved UID" username="ossec" password=NP group="ossec"
user ftpuser=false gcos-field="OSSEC Reserved Mail UID" username="ossecm" password=NP group="ossec"
user ftpuser=false gcos-field="OSSEC Reserved Remote UID" username="ossecr" password=NP group="ossec"

%files
%dir %attr (0755, root, ossec) /var/ossec
%defattr (-, root, ossec)
%dir %attr (0755, root, ossec) /var/ossec/queue
%dir %attr (0775, ossec, ossec) /var/ossec/queue/alerts
%dir %attr (0755, ossec, ossec) /var/ossec/queue/syscheck
%dir %attr (0770, ossec, ossec) /var/ossec/queue/ossec
%dir %attr (0750, ossec, ossec) /var/ossec/logs
%dir %attr (0664, ossec, ossec) /var/ossec/logs/ossec.log
%dir %attr (0775, ossec, ossec) /var/ossec/queue/rids
%dir %attr (0750, ossec, ossec) /var/ossec/queue/diff
%dir %attr (0755, ossec, ossec) /var/ossec/queue/agent-info
%dir %attr (0750, ossec, ossec) /var/ossec/queue/rootcheck
%dir %attr (0755, ossec, ossec) /var/ossec/queue/agentless
%dir %attr (0750, ossec, ossec) /var/ossec/queue/fts
%dir %attr (0550, root, ossec) /var/ossec/etc
%dir %attr (0770, root, ossec) /var/ossec/etc/shared
%dir %attr (0555, root, ossec) /var/ossec/etc/TIMEZONE
%dir %attr (0440, root, ossec) /var/ossec/etc/internal_options.conf
%dir %attr (0440, root, ossec) /var/ossec/etc/ossec.conf-example
%dir %attr (0644, root, ossec) /var/ossec/etc/ossec-init.conf
%dir %attr (0440, root, ossec) /var/ossec/etc/decoder.xml
%dir %attr (0555, root, ossec) /var/ossec/usr/
%dir %attr (0555, root, ossec) /var/ossec/usr/share
%dir %attr (0555, root, ossec) /var/ossec/usr/share/lib
%dir %attr (0555, root, ossec) /var/ossec/usr/share/lib/zoneinfo/
/var/ossec/usr/share/lib/zoneinfo/*
/var/ossec/etc/shared/*
/var/ossec/agentless/*
%dir %attr (0700, ossec, ossec) /var/ossec/.ssh
%dir %attr (0770, root, ossec) /var/ossec/var
%dir %attr (0770, root, ossec) /var/ossec/var/run
/var/ossec/active-response/bin/*
/var/ossec/bin/*
%dir %attr (0750, ossec, ossec) /var/ossec/stats
%dir %attr (0770, root, ossec) /var/ossec/logs/firewall
%dir %attr (0750, ossec, ossec) /var/ossec/logs/archives
%dir %attr (0750, ossec, ossec) /var/ossec/logs/alerts
%dir %attr (0550, root, ossec) /var/ossec/rules
/var/ossec/rules/*
%dir %attr (0550, root, ossec) /var/ossec/tmp

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/ossec.xml

%changelog
* Sun Mar 11 2012 - Logan Bruns <logan@gedanken.org>
- Added ossecm and ossecr users.
- Fixed some permissions.
* Thu Mar 1 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
