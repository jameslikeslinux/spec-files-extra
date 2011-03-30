#
# spec file for package SFEscribus
# Gilles Dauphin
# look at http://davekoelmeyer.wordpress.com/2010/03/09/build-scribus-1-3-5svn-on-opensolaris-x64/
#

# The stable release is 1.3.3.14.  This spec has not been tested with that.

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define srcname scribus

Name:           SFEscribus
Summary:        Graphical desktop publishing (DTP) application
Group:		Applications/Office
Version:        1.4.0.rc2
Source:		http://jaist.dl.sourceforge.net/project/%srcname/scribus-devel/%version/%srcname-%version.tar.bz2
Patch1:		scribus-01-math_c99.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
#Requires:	%name-root

BuildRequires: 	SFEqt47-gpp-devel
Requires: 	SFEqt47-gpp
Requires:	SFElibiconv

BuildRequires: 	SFEcmake
BuildRequires: 	SUNWPython

SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%description
Scribus is a GUI desktop publishing (DTP) application for Unix/Linux.


%prep
%setup -q -n %srcname-%version
%patch1 -p1
mkdir builddir

%build
cd builddir
# It's not worth trying to get this to build with Solaris Studio
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
# Use -D__C99FEATURES__ to get isfinite defined by iso/stlibc_99.h (patch1)
# Don't use -D_STDC_C99: that produces redefinition errors
# This is to avoid "error: `isfinite' is not a member of `std'"
export CXXFLAGS="%cxx_optflags -D__C99FEATURES__"
export LD="/usr/bin/ld"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
export PATH=/usr/g++/bin:$PATH
export QMAKESPEC=solaris-g++

# CMAKE_INSTALL_PREFIX is ignored by make install, but it does determine
# where Scribus looks for its icons.
# Use Qt Arthur, because library/desktop/cairo links to libpng12
cmake -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DPNG_PNG_INCLUDE_DIR:PATH=/usr/include/libpng14 -DCMAKE_INSTALL_PREFIX:PATH=%_prefix -DWANT_QTARTHUR=1 -DHAVE_GCC_VISIBILITY:INTERNAL=0 -DHAVE_VISIBILITY_SWITCH:INTERNAL=0 ..
make


%install
rm -rf $RPM_BUILD_ROOT
cd builddir
make install DESTDIR=%buildroot INSTALL="%_bindir/ginstall -c -p"

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_includedir}
# Todo
#%dir %attr(0755, root, other) %{_datadir}/applications
%{_bindir}/scribus
#TODO
#%{_datadir}/gnome/apps/Applications/scribus.desktop
%dir %attr(0755, root, root) %_datadir/mime
%dir %attr(0755, root, root) %_datadir/mime/packages
%{_datadir}/mime/packages/scribus.xml
# TODO
#%{_datadir}/pixmaps/scribus.png
#%{_datadir}/pixmaps/scribusicon.png
%{_datadir}/scribus
%{_includedir}/scribus/
%{_libdir}/scribus/
%dir %attr (-, root, other) %_docdir
%_docdir/scribus
%dir %attr(0755, root, root) %_datadir/mimelnk
%dir %attr(0755, root, root) %_datadir/mimelnk/application
%{_datadir}/mimelnk/application/*
%{_datadir}/man


%changelog
* 29 Mar 2011 - Alex Viskovatoff
- Update to 1.4.0.rc2; use SFEqt47-gpp and SFEcmake; use Qt Arthur
* 29 Apr 2010 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
- Initial spec
