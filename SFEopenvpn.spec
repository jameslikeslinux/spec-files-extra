#
# spec file for package SFEopenvpn
#
# includes module(s): openvpn
#
%include Solaris.inc
%include packagenamemacros.inc
%define srcname openvpn

Name:		SFEopenvpn
IPS_Package_Name:	system/network/openvpn
Summary:	Open source, full-featured SSL VPN package
Group:		System/Security
URL:		http://openvpn.net
License:	GPLv2
SUNW_copyright:	openvpn.copyright
Version:	2.2.2
Source:		http://swupdate.openvpn.net/community/releases/%srcname-%version.tar.gz
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElzo
Requires: SFElzo
BuildRequires: %{pnm_buildrequires_SUNWopenssl}
Requires: %{pnm_requires_SUNWopenssl}


%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/openvpn
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/openvpn.8
%dir %attr (0755, root, other) %dir %_docdir
%_docdir/%srcname

%changelog
* Tue Jul 24 2012 - Thomas Wagner
- change to (Build)Requires to %{pnm_buildrequires_SUNWopenssl}, %include packagenamacros.inc
* Mon Jul  2 2012 - Thomas Wagner
- bump to 2.2.2
* Wed Sep 28 2011 - Alex Viskovatoff
- Update to 2.2.1, fixing %files; add SUNW_copyright
- openssl is not in /usr/sfw
* Tue Jun 7 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 2.2.0, comes with integrated tun.c
* Wed Oct  3 2007 - Doug Scott <dougs@truemail.co.th>
- Added modified tun.c
* Wed Apr 07 2007 - Eric Boutilier
- Initial spec
