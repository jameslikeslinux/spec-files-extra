#
# spec file for package SFEdjvulibre
#
# includes module: djvulibre
#

%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define _cxx_libdir /usr/g++/lib
%define srcname djvulibre

Name:		SFEdjvulibre
IPS_Package_Name:	library/desktop/djvulibre
Summary:	Open source implementation of DjVu
URL:		http://djvu.sourceforge.net
Vendor:		The original inventors of DjVu
License:	GPLv2+
Group:		Desktop (GNOME)/Libraries
SUNW_Copyright:	djvulibre.copyright
Version:	3.5.25
Source:		%sf_download/project/djvu/DjVuLibre/%version/%srcname-%version.3.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEgcc

Requires:	SFEgccruntime

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# The developers of djvulibre recommend using gcc, so don't even try CC
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS="%_ldflags"

./configure --prefix=%_prefix --libdir=%_cxx_libdir

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_cxx_libdir/*.la

%if %build_l10n
%else
cd $RPM_BUILD_ROOT%_mandir
#rm -r cs de fr ja
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/*
%dir %attr (0755, root, bin) %_libdir
%_cxx_libdir/lib*.so*
%dir %attr (-, root, sys) %_datadir
%_datadir/djvu
%_mandir/man1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %attr (0755, root, other) %_includedir/libdjvu
%_includedir/libdjvu/*
%dir %attr (0755, root, other) %_cxx_libdir/pkgconfig
%_cxx_libdir/pkgconfig/ddjvuapi.pc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%_mandir/cs
%_mandir/de
%_mandir/fr
%_mandir/ja
%endif


%changelog
* Mon Aug 27 2012 - Milan Jurik
- bump to 3.5.25
* Sat Feb 04 2012 - Milan Jurik
- fix build with the latest GCC
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jun 12 2011 - Alex Viskovatoff
- Qt gcc libs are now in their own place
* Tue Apr 12 2011 - Alex Viskovatoff
- Bump to 3.5.24
* Tue Feb  8 2011 - Alex Viskovatoff
- Use /usr/stdcxx as basedir
* Mon Jan 31 2011 - Alex Viskovatoff
- Initial spec
