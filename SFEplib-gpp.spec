#
# spec file for package SFEplib	
# for games on OpenSolaris. Keep cool !!!
# Gilles Dauphin
#

%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name plib

Name:           SFEplib-gpp
IPS_Package_Name:	library/g++/plib
Summary:        plib , compile with gcc43
Version:        1.8.5
Source:		http://plib.sourceforge.net/dist/%{src_name}-%{version}.tar.gz
Patch1:		plib-01-sharelibs.diff
URL:		http://plib.sourceforge.net/
Group:		Applications/Games
License:        GPLv2
SUNW_Copyright: SFEplib.copyright
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
#Requires: 	SFEfreeglut
Requires: 	SUNWxorg-mesa
Requires: 	SUNWxwice
BuildRequires:	SUNWaudh

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

libtoolize --copy --force
./autogen.sh
./configure --prefix=%{_prefix}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}
%defattr (-, root, bin)
%{_includedir}/plib

%changelog
* May 18 2010 - Gilles Dauphin
- fork plib with gcc 4.3, needed for Flightgear and al..
* Mon May 03 2010 - Milan Jurik
- static libraries should be avoided, Debian patch makes dynamic libraries
* May 03 2010 - Gilles Dauphin
- get ready for next release
* Mon May 03 2010 - Milan Jurik
- fix packaging
* Fri Apr 30 2010 - Milan Jurik
- added missing build dependency
* Mars 02 2010 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
- no need of freeglut
* Nov 1 2008 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
* Initial spec, more funny tools for OpenSolaris ;)
