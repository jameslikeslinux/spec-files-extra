#
# spec file for package SFEopenconnect.spec
#
# includes module(s): openconnect
#

%include Solaris.inc
%include base.inc

%define src_name	openconnect

Name:		SFEopenconnect
IPS_Package_Name:	system/network/openconnect
Version:	3.13
Summary:	Open client for Cisco AnyConnect VPN
Group:		Productivity/Networking/Security
License:	LGPLv2+
URL:		http://www.infradead.org/openconnect.html
Source:		ftp://ftp.infradead.org/pub/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:		openconnect-01-locale.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires:	SFEtun
Requires:	SFEtun

%description
This package provides a client for Cisco's "AnyConnect" VPN, which uses
HTTPS and DTLS protocols.

%package devel
Summary:	%{summary} - developer files
Group:	Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%if %build_l10n
%package l10n
Summary:	 %{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build

CFLAGS="%{optflags} -D__sun__" LDFLAGS="%{_ldflags}" \
ZLIB_CFLAGS="-I/usr/include" ZLIB_LIBS=-lz \
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
	 --disable-static --enable-shared

make

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

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf %{buildroot}/%{_datadir}/locale
%endif

mkdir -p %{buildroot}%{_docdir}
mv %{buildroot}%{_datadir}/openconnect %{buildroot}%{_docdir}

rm -f %{buildroot}%{_libdir}/libopenconnect.la

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_bindir}/openconnect
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_datadir}/doc/openconnect
%{_mandir}/man1m/*
%{_libdir}/libopenconnect.so*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_includedir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Oct 06 2011 - Milan Jurik
- bump to 3.13
- add IPS package name
* Thu May 05 2011 - Knut Anders Hatlen
- Do not require gcc
* Mon May 02 2011 - Milan Jurik
- bump to 3.02
* Thu Dec 02 2010 - Milan Jurik
- Initial spec based on opensuse
