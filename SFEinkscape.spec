#
# spec file for package SFEinkscape
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): inkscape
#
%include Solaris.inc
%use poppler = poppler.spec
%define srcname inkscape

%define cc_is_gcc 1
%include base.inc

Name:		SFEinkscape
IPS_Package_Name:	image/editor/inkscape
Summary:	Vector graphics editor
Group:		Applications/Graphics and Imaging
License:	GPLv2
SUNW_Copyright:	inkscape.copyright
Version:	0.48.3.1
Source:		%{sf_download}/inkscape/inkscape-%{version}.tar.gz
URL:		http://www.inkscape.org
Patch1:		inkscape-01-open.diff
Patch2:		inkscape-02-makefile.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWgnome-libs
Requires:	SFEgtkmm-gpp
Requires:	SFEglibmm-gpp
Requires:	SFEsigcpp-gpp
Requires:	SFEpoppler-gpp
Requires:	SFEgsl
Requires:	SFElibgc-gpp
Requires:	SUNWlcms
Requires:	SFEboost-gpp
#Requires:	SFElibmagick-gpp
Requires:	SFElibwpg-gpp
BuildRequires:	SFEgtkmm-gpp-devel
BuildRequires:	SFEglibmm-gpp-devel
BuildRequires:	SFEsigcpp-gpp-devel
BuildRequires:	SFEpoppler-gpp-devel
BuildRequires:	SFEgsl-devel
BuildRequires:	SFElibgc-gpp-devel
BuildRequires:	SUNWgnome-libs-devel
BuildRequires:	SUNWPython26
BuildRequires:	SUNWlcms
BuildRequires:	SFEgtkmm-gpp-devel
BuildRequires:	SFEglibmm-gpp-devel
BuildRequires:	SFEsigcpp-gpp-devel
BuildRequires:	SFEboost-gpp-devel
#BuildRequires:	SFElibmagick-gpp-devel
BuildRequires:	SFElibwpg-gpp-devel
BuildRequires:  SUNWimagick-devel 
Requires:       SUNWimagick 

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd inkscape-%{version}
%patch1 -p1
%patch2 -p1
cd ../..
%poppler.prep -d %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I%{_builddir}/%name-%version/poppler-%{poppler.version} -I%{_builddir}/%name-%version/poppler-%{poppler.version}/poppler"
export CXXFLAGS="%cxx_optflags -fpermissive -I/usr/g++/include -I%{_builddir}/%name-%version/poppler-%{poppler.version} -I%{_builddir}/%name-%version/poppler-%{poppler.version}/poppler"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
# we need -L/usr/lib so that /usr/lib/libgc.so is picked up instead of
# SUNWspro's own libgc.so
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib %gnu_lib_path"

# Build poppler because the inkscape build requires poppler's config.h
%poppler.build

#export LDFLAGS="%{_ldflags} -L/usr/gnu/lib:/usr/g++/lib:%_builddir/%name-%version/poppler-%{poppler.version}/glib/.libs -lpoppler -R/usr/gnu/lib -R/usr/g++/lib"

cd %name-%version/inkscape-%version
#cd inkscape-%version
#glib-gettextize -f 
#libtoolize --copy --force
#intltoolize --copy --force --automake
#aclocal $ACLOCAL_FLAGS
#autoheader
#automake -a -c -f 
#autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

pushd src
sed -e 's/-xopenmp /-fopenmp /' -e 's/--export-dynamic//' Makefile > Makefile.new
#sed -e 's/-xopenmp /-fopenmp /' Makefile > Makefile.new
mv Makefile.new Makefile
make -j$CPUS 
#make

%install
rm -rf $RPM_BUILD_ROOT
cd inkscape-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/inkscape
%{_mandir}
%dir %attr (-, root, other) %_datadir/icons
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%_datadir/icons/hicolor/16x16/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22/apps
%_datadir/icons/hicolor/22x22/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24/apps
%_datadir/icons/hicolor/24x24/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48/apps
%_datadir/icons/hicolor/48x48/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/256x256
%dir %attr (-, root, other) %_datadir/icons/hicolor/256x256/apps
%_datadir/icons/hicolor/256x256/apps/%srcname.png

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Oct 15 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 0.48.3.1
- Migrated to SUNW vs SFE ImageMagick
* Sun Jul 1 2012 - Logan Bruns <logan@gedanken.org>
- fixed build requires SFEboost-gpp-devel instead of SFEboost-devel.
* Sat Jun 23 2012 - Logan Bruns <logan@gedanken.org>
- added %gnu_lib_path to LDFLAGS so the runpath for the gcc runtime is set
* Fri Dec 30 2011 - Milan Jurik
- fix 0.48.2 build, add libwpg
* Wed Dec 28 2011 - Milan Jurik
- reverting to 0.48.1 because previous bump was incomplete
* Tue Sep 27 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 0.48.2
* Tue Aug  9 2011 - Alex Viskovatoff
- SFElibgc now goes in /usr/g++
* Fri Aug  5 2011 - Alex Viskovatoff
- fix inkscape-01-combo.diff; use new g++ path layout; add missing dependency
  on SFEpoppler; use SFEgc; add SUNW_Copyright
* Wed Jun 8 2011 - Ken Mays <kmays2000@gmail.com>
- Added patches/inkscape-01-combo.diff
* Mon Jun 6 2011 - kmays2000@gmail.com
- bump to 0.48.1
* Wed Apr 23 2008 - laca@sun.com
- bump to 0.46
- update deps to build with SFE*-gpp
* Sat Feb  2 2008 - laca@sun.com
- bump to 0.45.1
- add patches aclocal.diff and isnormal.diff both fix build issues
- update %files lists - delete root pkg, add l10n pkg
* Tue Feb  6 2007 - damien.carbery@sun.com
- Bump to 0.45. Add Build/Requires SFElcms/-devel.
* Fri Oct 13 2006 - laca@sun.com
- bump to 0.44.1
* Thu Jul  6 2006 - laca@sun.com
- rename to SFEinkscape
- delete -share subpkg
- update file attributes
* Fri Mar 10 2006 - damien.carbery@sun.com
- Add Build/Requires for SUNWgtkmm, SUNWglibmm, SUNWsigcpp.
* Mon Jan 30 2006 - glynn.foster@sun.com
- Initial version
