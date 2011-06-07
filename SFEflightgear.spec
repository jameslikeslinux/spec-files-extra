#
# spec file for package SFEFlightGear.spec
# Gilles Dauphin
#
#
%include Solaris.inc

%define src_name	FlightGear
%define src_url		ftp://ftp.kingmont.com/flightsims/flightgear/Source/
#
# Mirror:
# ftp://ftp.de.flightgear.org/pub/fgfs/Source/FlightGear-1.0.0.tar.gz
# ftp://ftp.is.co.za/pub/games/flightgear/ftp/Source/FlightGear-1.0.0.tar.gz
#
# TODO: make package with:
# http://www.flightgear.org/Docs/getstart/getstart.html
# http://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Docs/getstart.pdf
#
# FlightGear Scenery package (Main Mirror)
# ftp://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Shared/fgfs-base-1.0.0.tar.bz2

%define SFEfreeglut  %(/usr/bin/pkginfo -q SFEfreeglut && echo 1 || echo 0)

Name:                   SFEFlightGear
Summary:                The multi-platform flight simulator development project
Version:                1.0.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			FlightGear-01.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SFEopenal-devel
Requires:		SFEopenal
BuildRequires:		SFEfreealut-devel
Requires:		SFEfreealut
# Take care: needed freeglut-2.6.0-rc1
%if %SFEfreeglut
BuildRequires:		SFEfreeglut-devel
Requires:		SFEfreeglut
%else
BuildRequires:		x11/library/freeglut
Requires:		x11/library/freeglut
%endif
BuildRequires:		SFESimGear-devel
Requires:		SFESimGear
#BuildRequires:		SFEplib-devel
Requires:		SFEplib

#%package root
#Summary:                 %{summary} - root files
#SUNW_BaseDir:            %{_prefix}
#%include default-depend.inc

%prep
#%setup -q -n -c %{src_name}-%{version}
%setup -q -c -n  %{name}
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}
export CC=cc
export CXX=CC
export CFLAGS="-I%_prefix/X11/include"
export CXXFLAGS="-I%_prefix/X11/include"
export LDFLAGS="-L%{_libdir} -R%{_libdir} -L/usr/X11/lib -R/usr/X11/lib"
#CC=cc CXX=CC ./configure --without-logging --prefix==%{_prefix}
/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix}
make # -j$CPUS 


%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

#%files devel
#%defattr (-, root, bin)
#%{_includedir}
#%dir %attr(0755,root,bin) %{_libdir}
#%dir %attr(0755,root,other) %{_libdir}/pkgconfig
#%{_libdir}/pkgconfig/*

%changelog
* Mon Jun 6 2011 - Ken Mays <kmays2000@gmail.com>
- Fixed Mirrors Link, Summary, and fgfs-base package link
- Fixed links for FlightGear 2.0.0 build review 
* Thu Feb 03 2011 - Milan Jurik
- SFEfreeglut as optinal
* Mar 2010 - Gilles Dauphin
- search includedir in /usr/SFE (exemple)
- that's where I install freeglut
* Mon Nov 20 2008 - dauphin@enst.fr
- Initial version
