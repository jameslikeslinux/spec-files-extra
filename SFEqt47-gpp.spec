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

# This spec is not intended to provide as much Qt functionality as
# SFEqt47.spec.  Its present purpose is merely to allow LyX to build
# and run on Solaris.  Thus few of the patches used by SFEqt47.spec
# are included.  In the future, one could see which of those patches
# would be useful here.

%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define srcname qt-everywhere-opensource-src

%include packagenamemacros.inc

Name:                SFEqt47-gpp
Summary:             Cross-platform development framework/toolkit
URL:                 http://trolltech.com/products/qt
License:             LGPLv2
Version:             4.7.2
Source:              ftp://ftp.trolltech.com/qt/source/%srcname-%version.tar.gz
Patch1:		     qt47/qt471-01-configure-ext.diff
Patch2:		     qt47/qt471-02-ext.diff
Patch3:		     qt47/qt472-03-ext2.diff
Patch4:		     qt47/qt471-04-sse42.diff
#These patches are stolen from KDE guys and affect WebKit 
#(I'm not first who stole them, most of them are stolen from cvsdude old repo)
Patch5:		     qt47/webkit01-17.diff
Patch6:		     qt47/webkit04-17.diff
Patch7:		     qt47/webkit05-17.diff
Patch8:		     qt47/webkit08-17.diff
Patch9:		     qt47/webkit10-17.diff
Patch10:	     qt47/webkit11-17.diff
Patch11:	     qt47/webkit13-17.diff
Patch12:	     qt47/webkit14-17.diff
Patch13:	     qt47/webkit15-17.diff
Patch14:	     qt47/webkit16-17.diff
Patch15:	     qt47/webkit17-17.diff
#These don't affect Webkit, I've decided they are nice and steal from KDE guys
Patch16:	     qt47/qt-fastmalloc.diff
Patch17:	     qt47/qt-align.diff 
Patch18:	     qt47/qt-qglobal.diff
Patch19:	     qt47/qt-4.6.2-iconv-XPG5.diff
Patch20: 	     qt47/qt-thread.diff
Patch21:	     qt47/qt-arch.diff 
Patch22:	     qt47/qt-4.6.2-webkit-CSSComputedStyleDeclaration.cpp.221.diff
Patch23:	     qt47/qt-4.6.2-networkaccessmanager.cpp.233.diff
Patch24:	     qt47/qt-4.7.0-webkit-runtime_array.h.234.diff
Patch25:	     qt47/qt-MathExtras.diff
Patch26:	     qt47/qt-webkit-exceptioncode.diff 
Patch27:	     qt47/qt-uistring.diff 
Patch28:	     qt47/template.diff 
Patch29:	     qt47/plugin-loader.diff 
Patch30:	     qt47/qt-qxmlquery.cpp.diff
Patch31:	     qt47/qt-clucene.diff 
Patch32:	     qt47/qt-configure-iconv.diff 
Patch33:	     qt47/qt-4.6.2-iconv.diff
Patch34:	     qt47/qt-qmutex_unix.cpp.diff
#These exclusive to SFE
Patch35:	     qt47/qt471-05-pluginqlib.diff
Patch36:	     qt47/qt-4.7.1-webkit-jscore-munmap.diff
Patch37:	     qt47/qt-4.7.1-webkit-jsc-wts-systemalloc.diff
Patch38:	     qt47/qt-4.7.1-mathextras.diff
Patch39: 	     qt47/qt-4.7.1-qiconvcodec.diff
Patch40:	     qt47/qt-471-shm.diff
Patch41:	     qt47/solaris-g++-qmake-conf.diff

SUNW_BaseDir:        %_basedir
BuildRoot:           %_tmppath/%name-%version-build
%include default-depend.inc

# Guarantee X/freetype environment concisely (hopefully):
BuildRequires: SUNWgtk2
Requires:      SUNWgtk2
Requires: SUNWxwplt
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2
# This package only provides libraries

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
# Don't pass --fuzz=0 to patch
%define _patch_options --unified
%patch1 -p0
%patch2 -p0
%patch3 -p1
%patch4 -p0
# %patch5 -p0
# %patch6 -p1
# %patch7 -p1
# %patch8 -p1
# %patch9 -p1
# %patch10 -p1
# %patch11 -p1
# %patch12 -p1
# %patch13 -p1
# %patch14 -p1
# %patch15 -p1
# %patch16 -p1
# %patch17 -p0
# %patch18 -p1
#%patch19 -p1
%patch20 -p0
# %patch21 -p0
# %patch22 -p1
# %patch23 -p1
# %patch24 -p1
# %patch25 -p0
# %patch26 -p0
%patch27 -p0
# %patch28 -p0
# %patch29 -p0
# %patch30 -p0
# %patch31 -p0
# %patch32 -p0
# %patch33 -p0
%patch34 -p1
# %patch35 -p0
# %patch36 -p0
# %patch37 -p0
# %patch38 -p0
%patch39 -p0
# %patch40 -p0


%build
CPUS=$(psrinfo | awk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export LD=/usr/gnu/bin/ld
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -I/usr/include/libpng14"
export LDFLAGS="%_ldflags -pthreads"

# Assume i386 CPU is not higher than Pentium
# This can be changed locally if your CPU is newer
echo yes | ./configure -prefix %_prefix \
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
	   -no-webkit \
           -no-exceptions \
           -sysconfdir %_sysconfdir \
           -L /usr/gnu/lib \
           -R /usr/gnu/lib \
	   -optimized-qmake \
	   -verbose

make -j$CPUS

%install
rm -rf %buildroot

make install INSTALL_ROOT=$RPM_BUILD_ROOT

rm %buildroot%_libdir/lib*a

# Eliminate QML imports stuff for now:
# Who is Nokia to create a new subdirectory in /usr?
rm -r %buildroot%_prefix/imports

# Patch qmake.conf to use our paths
cd %buildroot%_datadir/qt/mkspecs
%patch41 -p0


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
%_datadir/qt

%files -n %name-devel
%defattr (-, root, bin)
%_bindir
%dir %attr (0755, root, bin) %_includedir
%dir %attr (0755, root, other) %_includedir/qt
%{_includedir}/qt/*
%dir %attr (0755, root, bin) %dir %_libdir
%dir %attr (0755, root, other) %_libdir/pkgconfig 
%_libdir/pkgconfig/*

%files -n %name-doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/*


%changelog
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
