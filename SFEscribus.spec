#
# spec file for package SFEscribus
#

# The stable release is 1.3.3.14.  This spec has not been tested with that.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define src_name scribus

Name:           SFEscribus
IPS_Package_Name:	desktop/publishing/scribus
Summary:        Graphical desktop publishing (DTP) application
URL:		http://www.scribus.net/canvas/Scribus
Group:		Applications/Office
Version:        1.4.0
Source:		%{sf_download}/%{src_name}/%{version}/%src_name-%version.tar.bz2
License:	GPLv2
Patch1:		scribus-01-math_c99.diff
SUNW_BaseDir:   %_basedir
SUNW_Copyright: scribus.copyright
BuildRoot:      %_tmppath/%name-%version-build
%include	default-depend.inc
#Requires:	%name-root

BuildRequires: 	SFEqt-gpp-devel
Requires: 	SFEqt-gpp
BuildRequires:	SFElibiconv
Requires:	SFElibiconv
BuildRequires:	SUNWlcms
Requires:	SUNWlcms

BuildRequires: 	SFEcmake
BuildRequires: 	SUNWPython26
BuildRequires:  SUNWcupsu

SUNW_BaseDir:   %_basedir
%include default-depend.inc

%description
Scribus is a GUI desktop publishing (DTP) application for Unix/Linux.


%prep
%setup -q -n %src_name-%version
%patch1 -p1
mkdir builddir

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
cd builddir
# Don't even think about trying to build this with Solaris Studio
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

# Use Qt Arthur, because library/desktop/cairo links to libpng12
cmake -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DPNG_PNG_INCLUDE_DIR:PATH=/usr/include/libpng14 -DCMAKE_INSTALL_PREFIX:PATH=%_prefix -DWANT_QTARTHUR=1 -DHAVE_GCC_VISIBILITY:INTERNAL=0 -DHAVE_VISIBILITY_SWITCH:INTERNAL=0 ..
make -j$CPUS

%install
rm -rf %buildroot
cd builddir
make install DESTDIR=%buildroot INSTALL="%_bindir/ginstall -c -p"
cd ..
mkdir %buildroot%_datadir/applications
cp %src_name.desktop %buildroot%_datadir/applications

# Fix spaces in filenames
cd %buildroot%{_libdir}/scribus/swatches
for i in *' '*; do mv "$i" "`echo $i | sed -e 's/ /_/g'`"; done

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_bindir
%dir %attr (0755, root, bin) %_libdir
%dir %attr(0755, root, sys) %_datadir
%dir %attr(0755, root, bin) %_includedir
%dir %attr(0755, root, other) %_datadir/applications
%_datadir/applications/%src_name.desktop
%_bindir/scribus
#TODO
#%{_datadir}/gnome/apps/Applications/scribus.desktop
%dir %attr(0755, root, root) %_datadir/mime
%dir %attr(0755, root, root) %_datadir/mime/packages
%_datadir/mime/packages/scribus.xml
# TODO
#%{_datadir}/pixmaps/scribus.png
#%{_datadir}/pixmaps/scribusicon.png
%_datadir/scribus
%_includedir/scribus/
%_libdir/scribus/
%dir %attr (-, root, other) %_docdir
%_docdir/scribus
%dir %attr(0755, root, root) %_datadir/mimelnk
%dir %attr(0755, root, root) %_datadir/mimelnk/application
%_datadir/mimelnk/application/*
%_datadir/man


%changelog
* Sat Jun 23 2012 - Thomas Wagner
- make (Build)Requires SUNWcups SUNWlcms
* Sun Jan 08 2012 - Milan Jurik
- bump to 1.4.0
* Wed Nov  2 2011 - Alex Viskovatoff
- Bump to 1.4.0.rc6
* Tue Jul 26 2011 - Alex Viskovatoff
- Add missing (build) dependency
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* 26 Jun 2011 - Alex Viskovatoff
- Bump to 1.4.0.rc5
* 13 Apr 2011 - Alex Viskovatoff
- Update to 1.4.0.rc3; fix version name
* 29 Mar 2011 - Alex Viskovatoff
- Update to 1.4.0.rc2; use SFEqt47-gpp and SFEcmake; use Qt Arthur
* 29 Apr 2010 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
- Initial spec
