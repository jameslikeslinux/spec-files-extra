#
# spec file for package SFEopenconnect.spec
#
# includes module(s): openconnect
#

%include Solaris.inc
%include base.inc

%define src_name	openconnect

Name:		SFEopenconnect
Version:	3.02
IPS_component_version: 3.2
Summary:	Open client for Cisco AnyConnect VPN
Group:		Productivity/Networking/Security
License:	LGPLv2+
URL:		http://www.infradead.org/openconnect.html
Source:		ftp://ftp.infradead.org/pub/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:		openconnect-01-openssl.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:	SFEvpnc

%description
This package provides a client for Cisco's "AnyConnect" VPN, which uses
HTTPS and DTLS protocols.

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
make CC="$CC" RPM_OPT_FLAGS="%{optflags}" EXTRA_CFLAGS=-D__sun__

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
for i in %{buildroot}%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done
mkdir -p %{buildroot}/%{_mandir}/man1m
mv %{buildroot}/%{_mandir}/man8/* %{buildroot}/%{_mandir}/man1m/
rmdir %{buildroot}/%{_mandir}/man8

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%doc README.DTLS README.SecurID TODO COPYING.LGPL
%{_bindir}/openconnect
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_mandir}/man1m/*

%changelog
* Thu May 05 2011 - Knut Anders Hatlen
- Do not require gcc
* Mon May 02 2011 - Milan Jurik
- bump to 3.02
* Thu Dec 02 2010 - Milan Jurik
- Initial spec based on opensuse
