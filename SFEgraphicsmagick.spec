#
# spec file for package SFEgraphicsmagick.spec
#
# GraphicsMagick is a high-performance image processing package
# (originally based on ImageMagick) which focuses on stability,
# reliability, and performance while using a formal release process
# and providing a stable ABI.  See http://www.graphicsmagick.org/ for
# more information.
#
# includes module(s): graphicsmagick
#
%include Solaris.inc
%include packagenamemacros.inc

Name:                   SFEgraphicsmagick
Summary:                GraphicsMagick - Image Manipulation Utilities and Libraries
IPS_Package_Name:       image/editor/graphicsmagick
Group:                  Applications/Graphics and Imaging
License:                MIT
SUNW_copyright:         graphicsmagick.copyright
Version:                1.3.17
URL:			http://www.graphicsmagick.org/
Source:                 %{sf_download}/graphicsmagick/GraphicsMagick-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#%include perl-depend.inc

# JPEG-2000 library
BuildRequires:		SFEjasper-devel
Requires:		SFEjasper

# dcraw - Decoding RAW digital photos
# Stand-alone program. Not really a compile/link requirement
BuildRequires:		SUNWdcraw
Requires:		SUNWdcraw

# FreeType2 font handling library and rendering engine
BuildRequires:		SUNWfreetype2
Requires:		SUNWfreetype2

# The Zip compression library
BuildRequires:		SUNWzlib
Requires:		SUNWzlib

# jpeg - The Independent JPEG Groups JPEG software
BuildRequires:		SUNWjpg-devel
Requires:		SUNWjpg

# Portable Network Graphics library
BuildRequires:		SUNWpng-devel
Requires:		SUNWpng

# libtiff - library for reading and writing TIFF
BuildRequires:		SUNWTiff-devel
Requires:		SUNWTiff

# Little Color Management System (legacy API)
# Or could use SFElcms2 (modern API)
#BuildRequires:		SUNWlcms
#Requires:		SUNWlcms
BuildRequires:		SFElcms2
Requires:		SFElcms2

# The XML library
BuildRequires:		SUNWlxml-devel
Requires:		SUNWlxml

# X.Org Foundation X Client Libraries
BuildRequires:		SUNWxorg-clientlibs
Requires:		SUNWxorg-clientlibs

# Xorg server SDK headers
BuildRequires:		SUNWxorg-headers
Requires:		SUNWxorg-headers


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n GraphicsMagick-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# Check Solaris 10 and Solaris 11 freetype header locations
for dir in /usr/include/freetype2 /usr/sfw/include/freetype2 ; do
  if [ -d $dir ] ; then
    CPPFLAGS="$CPPFLAGS -I$dir"
    break
  fi
done
CPPFLAGS="$CPPFLAGS -I/usr/X11/include"
export CPPFLAGS

export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib"

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

if [ "x`basename $CC`" = xgcc ]
then
	%error "Building this spec with GCC is not supported."
fi
export CFLAGS="%optflags -xCC"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --with-perl			\
            --with-modules		\
            --with-quantum-depth=16     \
            --enable-shared		\
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a
find $RPM_BUILD_ROOT%{_libdir} -name lib\*.\*a -exec rm {} \;
# PerlMagic is broken
#site_perl=$RPM_BUILD_ROOT/usr/perl5/site_perl
#vendor_perl=$RPM_BUILD_ROOT/usr/perl5/vendor_perl
#mv $site_perl $vendor_perl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/GraphicsMagick-%{version}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/GraphicsMagick-%{version}
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/GraphicsMagick
# PerlMagic is broken
#%{_prefix}/perl5

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Oct 15 2012 - Ken Mays <kmays2000@gmail.com>
- update to 1.3.17
* Sun Aug 12 2012 - Bob Friesenhahn <bfriesen@simple.dallas.tx.us>
- Fully qualify actual dependencies.
- Find correct freetype headers for OS version.
- Use correct optimization options.
- Depend on SFElcms2 rather than SUNWlcms.
* Tue Jul 3 2012 - Bob Friesenhahn <bfriesen@simple.dallas.tx.us>
- bump to 1.3.16
* Mon Apr 28 2012 - Bob Friesenhahn <bfriesen@simple.dallas.tx.us>
- bump to 1.3.15
* Mon Apr 22 2012 - Bob Friesenhahn <bfriesen@simple.dallas.tx.us>
- bump to 1.3.14
* Mon Jan 2 2012 - Bob Friesenhahn <bfriesen@simple.dallas.tx.us>
- bump to 1.3.13
* Mon Oct 10 2011 - Alex Viskovatoff
- add --with-quantum-depth=16 (enables all features; changes library ABI)
- add SUNW_copyright and IPS_package_name
* Tue Feb  3 2011 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWsane_backend}
-  Requires to %{pnm_requires_SUNWsane_backend}
-  %include packagenamemacros.inc
* Sun Nov 07 2010 - Milan Jurik
- bump to 1.3.12, add Jasper to deps, disable PerlMagic because build is broken
* Tue Nov 17 2009 - bfriesen@simple.dallas.tx.us
- Update for GraphicsMagick 1.3.7.  Removed use of Solaris umem library.
* Thu Jan 24 2008 - bfriesen@simple.dallas.tx.us
- Update for GraphicsMagick 1.3.4.  Allow use of Solaris umem library.
* Thu Dec 11 2008 - bfriesen@simple.dallas.tx.us
- Update for GraphicsMagick 1.3.3.
* Tue Dec 2 2008 - bfriesen@simple.dallas.tx.us
- Update for GraphicsMagick 1.3.2.
* Sun Aug 3 2008 - bfriesen@simple.dallas.tx.us
- Update for GraphicsMagick 1.2.5.
* Mon Jan 28 2008 - moinak.ghosh@sun.com
- Initial spec.
