#
# spec file for package SFEminiupnpd
#
# includes module(s): miniupnpd
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define _basedir /
%define srcname miniupnpd

Name:                    SFEminiupnpd
IPS_Package_Name:	 network/miniupnpd
Summary:                 miniupnpd - UPnP Internet Gateway Device Daemon
Group:                   Utility
Version:                 1.6.20120207
URL:		         http://miniupnp.free.fr
Source:		         http://miniupnp.free.fr/files/%srcname-%version.tar.gz
Source2:                 miniupnpd.xml
License: 		 BSD
Patch1:                  miniupnpd-01-makefile.diff
Patch2:                  miniupnpd-02-max.diff
Patch3:                  miniupnpd-03-salen.diff
Patch4:                  miniupnpd-04-syslog.diff
Patch5:                  miniupnpd-05-syslog.diff
Patch6:                  miniupnpd-06-syslog.diff
Patch7:                  miniupnpd-07-max-uint64t.diff
Patch8:                  miniupnpd-08-upnpredirect.diff
Patch9:                  miniupnpd-09-ipf5-updates.diff
Patch10:                 miniupnpd-10-upnpredirect.diff
Patch11:                 miniupnpd-11-ignore-link-level.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEipf

%description
The MiniUPnP project offers software which supports the UPnP Internet
Gateway Device (IGD) specifications. Recently, NAT-PMP support was
added to MiniUPnPd.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

cp -p %{SOURCE2} miniupnpd.xml

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

make config.h
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/etc/miniupnpd.conf $RPM_BUILD_ROOT/etc/miniupnpd.conf.example
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1/
cp miniupnpd.1 $RPM_BUILD_ROOT/usr/share/man/man1/
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp miniupnpd.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
/sbin/miniupnpd
/etc/miniupnpd.conf.example
/usr/share/man/man1/miniupnpd.1
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/miniupnpd.xml

%changelog
* Sat Mar 3 2012- Logan Bruns <logan@gedanken.org>
- Added a smf manifest.
* Tue Feb 28 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
