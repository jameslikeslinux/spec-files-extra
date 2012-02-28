#
# spec file for package SFEipf
#
# includes module(s): ipf
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define _basedir /
%define srcname ip_fil

Name:                    SFEipf
IPS_Package_Name:	 sfe/network/ipfilter
Summary:                 IP Filter - TCP/IP Firewall/NAT Software
Group:                   Utility
Version:                 5.1.1
URL:		         http://coombs.anu.edu.au/~avalon/
Source:		         http://coombs.anu.edu.au/~avalon/%{srcname}%{version}.tar.gz
Source2:                 ipfilter.xml
License: 		 GPLv2
Patch1:                  ipf-01-ipsend.diff
Patch2:                  ipf-02-enable-statetop.diff
Patch3:                  ipf-03-workaround-zone-kernel-check.diff
Patch4:                  ipf-04-xmodel-kernel.diff
Patch5:                  ipf-05-ipfboot-etc-ipf.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
IPFilter is a software package that can be used to provide network
address translation (NAT) or firewall services. To use, it can either
be used as a loadable kernel module or incorporated into your UNIX
kernel; use as a loadable kernel module where possible is highly
recommended. Scripts are provided to install and patch system files,
as required.

%prep
rm -rf %name-%version
%setup -q -n %srcname%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
/usr/ccs/bin/make solaris MAKE=/usr/ccs/bin/make CC="$(CC)"

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
CPUDIR=`uname -p`-`uname -r`
cd SunOS5
/usr/ccs/bin/make $CPUDIR/ipf.pkg
mv $CPUDIR/root/* $RPM_BUILD_ROOT/
for f in $RPM_BUILD_ROOT/sbin/*/* ; do
    cp /usr/lib/isaexec $RPM_BUILD_ROOT/sbin/`basename $f`
done
for f in $RPM_BUILD_ROOT/opt/ipf/bin/*/* ; do
    cp /usr/lib/isaexec $RPM_BUILD_ROOT/opt/ipf/bin/`basename $f`
done
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp -p %{SOURCE2} ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%post
( retval=0; 
  /usr/sbin/add_drv ipf || retval=1;
  exit $retval
)

%preun
( retval=0;
  /usr/sbin/rem_drv ipf || retval=1;
  exit $retval
)

%files
%defattr (-, root, bin)
/etc/init.d/ipfboot
/opt/ipf/bin/*
/opt/ipf/examples/*
/opt/ipf/man/man*/*
/sbin/*
%dir %attr(0755, root, bin) /usr/include/ipfilter
/usr/include/ipfilter/*
%dir %attr(0755, root, bin) /usr/kernel/drv/ipf.conf
%dir %attr(0755, root, bin) /usr/kernel/drv/*/ipf
%class(manifest) %attr(0444, root, sys) /var/svc/manifest/site/ipfilter.xml

%changelog
* Tue Feb 28 2012- Logan Bruns <logan@gedanken.org>
- Fix isaexec usage.
* Mon Feb 27 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
