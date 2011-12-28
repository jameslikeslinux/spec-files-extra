#
# spec file for package SFElcab.spec
#
# includes module(s): lcab
#
%include Solaris.inc

%define src_name	lcab

Name:		SFElcab
IPS_Package_Name:	compress/lcab
Summary:                Microsoft cabinet file creator
Version:                1.0b12
IPS_Component_Version:	1.0.12
Source:                 ftp://ohnopublishing.net/mirror/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -n %{src_name}-%{version}
autoreconf
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} 
%build
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%changelog
* Mars 24 2010 - Gilles Dauphin
- IPS versionning
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Fixed links
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

