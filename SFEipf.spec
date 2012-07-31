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
Patch6:                  ipf-06-multicast-bug.diff
Patch7:                  ipf-07-ipfboot-in-zone.diff
Patch8:                  ipf-08-ipfstat.diff
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
%patch6 -p1
%patch7 -p1
%patch8 -p1

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
mv $CPUDIR/root/etc $RPM_BUILD_ROOT/
mv $CPUDIR/root/sbin $RPM_BUILD_ROOT/
mv $CPUDIR/root/usr $RPM_BUILD_ROOT/
mv $RPM_BUILD_ROOT/usr/include/ipfilter $RPM_BUILD_ROOT/usr/include/netinet
cp ../ipl.h $RPM_BUILD_ROOT/usr/include/netinet/
cp ../ipf_rb.h $RPM_BUILD_ROOT/usr/include/netinet/
mv $CPUDIR/root/opt/ipf/bin $RPM_BUILD_ROOT/usr/sbin
mkdir $RPM_BUILD_ROOT/usr/share
mv $CPUDIR/root/opt/ipf/man $RPM_BUILD_ROOT/usr/share
mv $CPUDIR/root/opt/ipf $RPM_BUILD_ROOT/usr/share
for f in $RPM_BUILD_ROOT/sbin/*/* ; do
    rm -f $RPM_BUILD_ROOT/sbin/`basename $f`
    cp /usr/lib/isaexec $RPM_BUILD_ROOT/sbin/`basename $f`
done
for f in $RPM_BUILD_ROOT/usr/sbin/*/* ; do
    rm -f $RPM_BUILD_ROOT/usr/sbin/`basename $f`
    cp /usr/lib/isaexec $RPM_BUILD_ROOT/usr/sbin/`basename $f`
done
mkdir $RPM_BUILD_ROOT/etc/ipf
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
%dir %attr(0755, root, sys) /etc
%dir %attr(0755, root, sys) /etc/init.d
/etc/init.d/ipfboot
%dir %attr(0755, root, sys) /usr
%dir %attr(0755, root, sys) /usr/share
%dir %attr(0755, root, other) /usr/share/ipf
%dir %attr(0755, root, other) /usr/share/ipf/examples
/usr/share/ipf/examples/*
%dir %attr(0755, root, bin) /usr/share/man
%dir %attr(0755, root, bin) /usr/share/man/man1
/usr/share/man/man1/*
%dir %attr(0755, root, bin) /usr/share/man/man4
/usr/share/man/man4/*
%dir %attr(0755, root, bin) /usr/share/man/man5
/usr/share/man/man5/*
%dir %attr(0755, root, bin) /usr/share/man/man8
/usr/share/man/man8/*
%dir %attr(0755, root, bin) /sbin
/sbin/*
%dir %attr(0755, root, bin) /usr/sbin
/usr/sbin/*
%dir %attr(0755, root, bin) /usr/include
%dir %attr(0755, root, bin) /usr/include/netinet
/usr/include/netinet/*.h
%dir %attr(0755, root, sys) /usr/kernel
%dir %attr(0755, root, sys) /usr/kernel/drv
%dir %attr(0755, root, bin) /usr/kernel/drv/ipf.conf
%dir %attr(0755, root, sys) /usr/kernel/drv/amd64
%dir %attr(0755, root, bin) /usr/kernel/drv/*/ipf
%dir %attr(0755, root, bin) /etc/ipf
%dir %attr(0755, root, sys) /var
%dir %attr(0755, root, sys) /var/svc
%dir %attr(0755, root, sys) /var/svc/manifest
%dir %attr(0755, root, sys) /var/svc/manifest/site
%class(manifest) %attr(0444, root, sys) /var/svc/manifest/site/ipfilter.xml

%changelog
* Sat May 12 2012 - Logan Bruns <logan@gedanken.org>
- Fixed a permission.
* Mon Apr 30 2012 - Logan Bruns <logan@gedanken.org>
- Fix some permissions.
* Sun Mar 11 2012 - Logan Bruns <logan@gedanken.org>
- Fixed a ull formatting issue in ipfstat -t output. (Resulting from
  using curses instead of ncurses.)
* Tue Mar 6 2012 - Logan Bruns <logan@gedanken.org>
- Added multicast bug fix patch from Darren and patched ipfboot to work in a zone.
* Sat Mar 3 2012 - Logan Bruns <logan@gedanken.org>
- Create empty /etc/ipf directory.
* Tue Feb 28 2012- Logan Bruns <logan@gedanken.org>
- Fix isaexec usage. Moved /opt/ipf documents, example and test pieces
  under /usr/share and /usr/sbin. Also moved headers to be in the same
  place as default distribution.
* Mon Feb 27 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
