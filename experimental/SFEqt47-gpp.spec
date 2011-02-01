#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

# This spec is not intended to provide as much Qt functionality as
# SFEqt47.spec.  Its present purpose is merely to allow LyX to build
# and run on Solaris.

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define srcname qt-everywhere-opensource-src

Name:                SFEqt47-gpp
Summary:             Cross-platform development framework/toolkit
URL:                 http://trolltech.com/products/qt
License:             LGPLv2
Version:             4.7.1
Source:              ftp://ftp.trolltech.com/qt/source/%{srcname}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#FIXME: Requires: SUNWxorg-mesa
# Guarantee X/freetype environment concisely (hopefully):
Requires: SUNWGtku
Requires: SUNWxwplt
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2
# This package only provides libraries
Requires: SFEqt47

# %package devel
# Summary:        %{summary} - development files
# SUNW_BaseDir:   %{_basedir}
# %include default-depend.inc
# Requires: %name

%prep
%setup -q -n %{srcname}-%version


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export LD=/usr/gnu/bin/ld
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -I/usr/include/libpng14"
export LDFLAGS="%_ldflags"

# Assume i386 CPU is not higher than Pentium
# This can be changed locally if your CPU is newer
echo yes | ./configure -prefix %{_prefix} \
           -no-sse -no-sse2 -no-ssse3 -no-sse4.1 -no-sse4.2 \
           -platform solaris-g++ \
           -opensource \
           -docdir %{_docdir}/qt \
	   -bindir %_bindir \
	   -libdir %_cxx_libdir \
           -headerdir %{_includedir}/qt \
           -plugindir %{_cxx_libdir}/qt/plugins \
           -datadir %{_datadir}/qt \
           -translationdir %{_datadir}/qt/translations \
           -nomake examples \
           -nomake demos \
           -no-phonon \
           -no-phonon-backend \
	   -no-webkit \
           -no-exceptions \
           -sysconfdir %{_sysconfdir} \
           -L /usr/gnu/lib \
           -R /usr/gnu/lib \
	   -optimized-qmake \
	   -verbose 		

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install_subtargets INSTALL_ROOT=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_cxx_libdir}/lib*a

# remove files included in SUNWqt47-devel:
rm -r $RPM_BUILD_ROOT%_datadir
rm -rf $RPM_BUILD_ROOT%_includedir
rm -r ${RPM_BUILD_ROOT}%_bindir

# Eliminate QML imports stuff for now:
# Who is Nokia to create a new subdirectory in /usr?
rm -r ${RPM_BUILD_ROOT}%_prefix/imports

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*.so*
%{_cxx_libdir}/lib*.prl
%dir %attr (0755, root, bin) %{_cxx_libdir}/qt
%{_cxx_libdir}/qt/*

#%files devel
#%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %dir %{_cxx_libdir} 
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig 
%{_cxx_libdir}/pkgconfig/*

%changelog
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
