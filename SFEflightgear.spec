#
# spec file for package SFEFlightGear.spec
# Gilles Dauphin
#
#

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++

%define src_name	flightgear
%define src_url		ftp://ftp.kingmont.com/flightsims/flightgear/Source

#
# Mirror:
# ftp://ftp.kingmont.com/flightsims/flightgear/Source/flightgear-2.6.0.tar.bz2
# http://ftp.linux.kiev.ua/pub/fgfs/Source/flightgear-2.6.0.tar.bz2
# ftp://ftp.de.flightgear.org/pub/fgfs/Source/flightgear-2.6.0.tar.bz2 
# ftp://ftp.is.co.za/pub/games/flightgear/ftp/Source/flightgear-2.6.0.tar.bz2
#
# TODO: make package with:
# http://www.flightgear.org/Docs/getstart/getstart.html
# http://mapserver.flightgear.org/getstart.pdf
#
# FlightGear Scenery package (Main Mirror)
# ftp://ftp.de.flightgear.org/pub/fgfs/Shared/FlightGear-data-2.6.0.tar.bz2
#
# FlightGear Aircraft files (Mirror)
# ftp://ftp.de.flightgear.org/pub/fgfs/Aircraft-2.6/
#
# FlightGear Scenery
# ftp://ftp.de.flightgear.org/pub/fgfs/Scenery-v2.6.0/
#
Name:                   SFEFlightGear
Summary:                The multi-platform flight simulator development project
Version:                2.6.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Source1:		ftp://ftp.de.flightgear.org/pub/fgfs/Shared/FlightGear-data-%{version}.tar.bz2 
Group:			Applications/Games
#Patch1:			FlightGear20-04.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:  SFEopenal-devel
Requires:       SFEopenal
BuildRequires:  SFEfreealut-devel
Requires:       SFEfreealut
BuildRequires:  SFEplib-gpp-devel
Requires:       SFEplib-gpp
BuildRequires:  SFEosg-devel
Requires:       SFEosg
BuildRequires:  SFEboost-gpp-devel
Requires:       SFEboost-gpp
BuildRequires:  SFEfreeglut-devel
Requires:       SFEfreeglut
BuildRequires:  SFEsimgear-devel
Requires:       SFEsimgear

%prep
%setup -q -c -n  %{name}
#%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CFLAGS="-I%{_prefix}/X11/include"
export CXXFLAGS="-I%{_prefix}/X11/include"
export LDFLAGS="-L%{_libdir} -R%{_libdir} -L/usr/X11/lib -R/usr/X11/lib"

# FlightGear 2.6.0 uses CMake >=2.6.4
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix}

# FlightGear 2.4.0 
#/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix} \
	--with-osg=%{_prefix} \
	--with-boost=%{_prefix} \
	--with-boost-libdir=%{_libdir} \
	--with-plib=%{_prefix} \
	--with-simgear=%{_prefix}

make # -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/FlightGear
(cd $RPM_BUILD_ROOT/%{_datadir}/FlightGear ; gtar xfj %{SOURCE1} )


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/FlightGear
%{_datadir}/FlightGear/*
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*


%changelog
* Mon Mar 05 2012 - Ken Mays <kmays2000@gmail.com>
- Fixed for new SFEsimgear.spec
* Sat Mar 03 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 2.6.0
* Wed Sep 14 2011 - Thomas Wagner
- back to SFE default compiler location /usr/gnu/bin/gcc
  agreed with Ken on IRC
* Tue Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- Minor tweaks
* Fri Sep 02 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2.4.0
* Mon Jun 6 2011 - Ken Mays <kmays2000@gmail.com>
- Cleanup and Summary fixes 
* May 2010 - G.D.
- update to 2.0
* Mar 2010 - Gilles Dauphin
- search includedir in /usr/SFE (exemple)
- that's where I install freeglut
* Mon Nov 20 2008 - dauphin@enst.fr
- Initial version
