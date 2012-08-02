#
# spec file for package SFEbullet.spec
#
# includes module(s): bullet
#
%include Solaris.inc

%define src_name	bullet
%define src_url		http://bullet.googlecode.com/files

%define SFEfreeglut  %(/usr/bin/pkginfo -q SFEfreeglut && echo 1 || echo 0)

Name:		SFEbullet
IPS_Package_Name:	library/bullet
Summary:	Bullet Physics Library
Group:		System/Libraries
License:	BSD3c
SUNW_Copyright:	bullet.copyright
Version:	2.77
URL:		http://code.google.com/p/bullet/
Source:		%{src_url}/%{src_name}-%{version}.tgz
Patch1:		bullet-01-gcc.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}b-build
%include default-depend.inc
BuildRequires: SFEjam
%if %SFEfreeglut
BuildRequires: SFEfreeglut-devel
Requires: SFEfreeglut
%else
BuildRequires: x11/library/freeglut
Requires: x11/library/freeglut
%endif
BuildRequires: SFEcmake
BuildRequires: SFEgcc
Requires: SFEgccruntime

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I/usr/X11/include"
export CC=gcc
export CXX=g++
export CFLAGS="-O2 -fno-omit-frame-pointer -I%{_prefix}/X11/include "
export CXXFLAGS="-O2 -fno-omit-frame-pointer -fpermissive -I%{_prefix}/X11/include "
export LDFLAGS="-R%{_libdir} -L%{_libdir} -lX11 "

./autogen.sh
./configure --prefix=%{_prefix} --enable-shared --disable-static --disable-demos

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}
%{_libdir}/*so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Jul 26 2011 - Alex Viskovatoff
- add -fpermissive to CXXFLAGS to allow build with gcc 4.6
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sat Feb 05 2011 - Milan Jurik
- bump to 2.77
- avoid cmake, build extras and dynamic libs
* Thu Feb 03 2011 - Milan Jurik
- SFEfreeglut as optinal
* May 2010 - Gilles DAuphin
- bump release
* Mar 2010 - Gilles Dauphin
- shared is the default
- jam is in _bindir
* Jul 2009 - Gilles Dauphin
- version is b
* April 2008 - Gilles Dauphin
- adjust name for IPS
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
