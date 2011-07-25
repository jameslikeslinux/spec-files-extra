#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

# NOTE: The easiest way to make pkgtool find the patches used by this spec
# is to install experimental/SFEpkgbuild.spec, and rename pkgbuild and pkgtool
# in /opt/dtbld/bin to something else, so that your updated pkgbuild and
# pkgtool are found instead.
# Otherwise, build with
# pkgtool build --patches=patches/qt47 SFEqt47-gpp.spec
# If you use the --autodeps flag, use
# pkgtool build --patches=patches:patches/qt47-gpp --autodeps SFEqt47.spec

%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define srcname qt-everywhere-opensource-src
%define patchprefix qt-gpp
%define run_autotests 0

%include packagenamemacros.inc

Name:                SFEqt47-gpp
Summary:             Cross-platform development framework/toolkit
Group:               Desktop (GNOME)/Libraries
URL:                 http://trolltech.com/products/qt
License:             LGPLv2
Version:             4.7.3
Source:              ftp://ftp.trolltech.com/qt/source/%srcname-%version.tar.gz

# These were obtained from http://solaris.bionicmutton.org/hg/kde4-specs-470/file/db0a8c7904f6/specs/gcc/patches/qt
# For Patch3, we use our own, which sets the SFE /usr/g++ paths
Patch1:		%patchprefix/qt-gc-sections.diff
Patch2:		%patchprefix/qt-MathExtras.diff
Patch3:		%patchprefix/qt-qmake.SFE.diff

# This is required to build with gcc 4.6.1
Patch6:		%patchprefix/qt-isnan.diff

%if %{run_autotests}
Patch4:		%patchprefix/qt-tests-auto-qwidget_window.diff
#from upstream
Patch5:		%patchprefix/qt-auto-tests-qhttpnetworkconnection.diff
%endif

SUNW_Copyright:	     qt.copyright
SUNW_BaseDir:        %_basedir
BuildRoot:           %_tmppath/%name-%version-build
%include default-depend.inc
BuildRequires:		SFEgcc
Requires:		SFEgccruntime

# Guarantee X/freetype environment concisely (hopefully):
BuildRequires: SUNWgtk2
Requires:      SUNWgtk2
Requires: SUNWxwplt
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2
# This package only provides libraries
BuildRequires: database/mysql-51
Requires: database/mysql-51

#detected by ldding the binaries
Requires: database/mysql-51/library,image/library/libjpeg,image/library/libpng,image/library/libtiff,library/glib2,library/libxml2,library/zlib,service/opengl/ogl-select,system/library,system/library/c++/sunpro,system/library/math,x11/library/libice,x11/library/libsm,x11/library/libx11,x11/library/libxdamage,x11/library/libxext,x11/library/libxrender,x11/library/mesa 

%package -n %name-devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package -n %name-doc
Summary:        %{summary} - documentation files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version

%if %{run_autotests}
# Unroll the extra source for the autotests
tar xzf %{SOURCE1}
%endif

# Don't pass --fuzz=0 to patch
%define _patch_options --unified
%patch1
%patch2
%patch3
%patch6 -p1
%if %{run_autotests}
%patch4
%patch5
%endif


%build
CPUS=$(psrinfo | awk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

#%define extra_includes -I/usr/include/libmng -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -I/usr/include/libpng12 -I/usr/mysql/5.1/include/mysql
%define extra_includes -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -I/usr/include/libpng14 -I/usr/mysql/5.1/include/mysql
%define extra_libs -L/usr/mysql/5.1/lib/mysql -R/usr/mysql/5.1/lib/mysql

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export LD=/usr/gnu/bin/ld
export CFLAGS="%optflags"
#export CXXFLAGS="%cxx_optflags -pthreads -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -I/usr/include/libpng14"
export CXXFLAGS="%cxx_optflags -pthreads"
export LDFLAGS="%_ldflags -pthreads"

# Assume i386 CPU is not higher than Pentium
# This can be changed locally if your CPU is newer
./configure -prefix %_prefix \
           -confirm-license \
           -no-ssse3 -no-sse4.1 -no-sse4.2 \
           -platform solaris-g++ \
           -opensource \
           -docdir %_docdir/qt \
	   -bindir %_bindir \
	   -libdir %_libdir \
           -headerdir %_includedir/qt \
           -plugindir %_libdir/qt/plugins \
           -datadir %_datadir/qt \
           -translationdir %_datadir/qt/translations \
           -nomake examples \
           -nomake demos \
	   -webkit \
           -no-exceptions \
           -sysconfdir %_sysconfdir \
           -L /usr/gnu/lib \
           -R /usr/gnu/lib \
	   -optimized-qmake \
           -reduce-relocations \
           -opengl desktop \
          -shared \
           %extra_includes \
           %extra_libs


make -j$CPUS

%if %{run_autotests}
#running autotests. This requires a vncserver preconfigured.
#According to docs, we should have a KDE session running, so far it does not seem necessary for most of the tests.
export QTDIR=${PWD}
export QTSRCDIR=${PWD}
export PATH=${PWD}/bin:${PATH}

cd tests/auto

gmake
vncserver -kill :1 || true
vncserver :1
export DISPLAY=:1
./test.pl . U
vncserver -kill :1
#hopefully this will break the build
#false
%endif


%install
rm -rf %buildroot

make install INSTALL_ROOT=$RPM_BUILD_ROOT

rm %buildroot%_libdir/lib*a

# Eliminate QML imports stuff for now:
# Who is Nokia to create a new subdirectory in /usr?
rm -r %buildroot%_prefix/imports


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_libdir
%_libdir/lib*.so*
%_libdir/lib*.prl
%dir %attr (0755, root, bin) %_libdir/qt
%_libdir/qt/*
%dir %attr (0755, root, sys) %_datadir
%_datadir/qt/phrasebooks
%_datadir/qt/translations

%files -n %name-devel
%defattr (-, root, bin)
%_bindir
%dir %attr (0755, root, bin) %_includedir
%dir %attr (0755, root, other) %_includedir/qt
%{_includedir}/qt/*
%dir %attr (0755, root, bin) %dir %_libdir
%dir %attr (0755, root, other) %_libdir/pkgconfig 
%_libdir/pkgconfig/*
%dir %attr (0755, root, sys) %_datadir
%_datadir/qt/mkspecs

%files -n %name-doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%_datadir/qt/q3porting.xml
%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/*


%changelog
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Mon Jul 18 2011 - Alex Viskovatoff <hezen@imap.cc>
- Add patch qt-isnan.diff to enable building with gcc 4.6
* Sat Jul  2 2011 - Alex Viskovatoff <hezen@imap.cc>
- Add missing dependency on SFEgcc
* Sat Jun 25 2011 - Alex Viskovatoff <hezen@imap.cc>
- Use patches from kde-solaris instead of those inherited from SFEqt47.spec
- Bump to 4.7.3
* Wed Mar 30 2011 - Alex Viskovatoff
- update to 4.7.2; create separate doc package
* Tue Mar 29 2011 - Thomas Wagner
- re-add %package and %files -n %name-devel, easier to have a complete package
- change BuildRequires to %{pnm_buildrequires_library_desktop_gtk1}
* Mar 23 2011 - Alex Viskovatoff
- Use /usr/g++ as basedir, not sharing headers with stdcxx anymore
* Feb  8 2011 - Alex Viskovatoff
- Use /usr/stdcxx as basedir; use -pthreads
* Jan 30 2011 - Alex Viskovatoff
- Do not bother with a separate devel SVr4 package, as it is only 50 K
* Nov 30 2010 - Alex Viskovatoff
- Fork SFEqt47-gpp.spec off SFEqt47.spec, not packaging files in
  _datadir, _include_dir, and _bindir.  Those are in SFEqt47.
* Nov 17 2010 - Alex Viskovatoff
- Add patch by russiane39 to correctly use libpng14 headers under snv_151
  and adding some configure options
* Nov 11 2010 - Alex Viskovatoff
- Fork SFEqt47.spec off SFEqt4.spec, disregarding stlport and snv < 147
- To make the build work, disable examples and phonon.  Disable demos
  because that is what kde-solaris does.
* Nov  4 2010 - Alex Viskovatoff
- Spec needs "%include osdistro.inc" (pointed out by Thomas Wagner)
* Nov  3 2010 - Alex Viskovatoff
- Add patch by Milan Jurik to use new libpng names only for osbuild >= 147
- Use cxx_optflags
* Oct 16 2010 - Alex Viskovatoff
- Fix broken use of stlport: if -library=stlport4 is passed to the compiler,
  it must also be passed to the linker
- Update to version 4.5.3, obviating the need for the existing patches
- Add a patch to use changed field names in libpng-1.4
- Use stdcxx instead of stlport, while allowing use of the deprecated
  stlport as an option. (BionicMutton uses stdcxx.)
- Remove dependency on SUNWgccruntime
* Mar 07 2009 - Thomas Wagner
- rework shared patch qt-01-use_bash.diff (to be more independent of qt version SFEqt SFEqt4 in verison 4.x / 4.5)
* Wed Mar 04 2009 - Thomas Wagner
- fix path to SunStudio compiler. Tested with SunStudioExpress November 2008 in /opt/SUNWspro/bin
- enable configure's hint -no-exceptions (smaller code, less memory)
* Sat Nov 29 2008 - dauphin@enst.fr
- Try to compile with studio12
* Mon Nov 24 2008 - alexander@skwar.name
- Add qt-01-use_bash.diff, which replaces all calls to sh with bash,
  because Qt won't build when sh isn't bash.
  Cf. http://markmail.org/message/hzb3fypsc5sopf2b ff. and there
  http://markmail.org/message/l7yleonbjqnl7nfv
- Remove tarball_version - version is good enough
* Sun Nov 11 2008 - dick@nagual.nl
- Bump to 4.4.3
* Sun Sep 21 2008 - dick@nagual.nl
- Bump to 4.4.2
* Tue May 13 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0
* Fri Mar 21 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0-rc1
- Remove upstreamed patch time.diff
* Fri Mar 21 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0-beta1, and update %files
- Add patch time.diff
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
- Bump to 4.2.3
* Thu Dec 07 2006 - Eric Boutilier
- Initial spec
