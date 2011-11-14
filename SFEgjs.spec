
# spec file for package SFEgjs
#
# includes module(s): gjs
#
%include Solaris.inc
Name:                    SFEgjs
Summary:                 GNOME JavaScript bindings
Version:                 1.30.0
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gjs/1.30/gjs-%{version}.tar.bz2
# see b.g.o 619721 and 595447
Patch1:                  gjs-01-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SUNWgobject-introspection-devel
BuildRequires:           SUNWspidermonkey-devel
Requires:                SUNWglib2
Requires:                SUNWdbus-glib
Requires:                SUNWgobject-introspection
Requires:                SUNWspidermonkey
# Need nspr.pc file in SUNWprd
BuildRequires:           SUNWprd
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
%setup -q -n gjs-%version
%patch1 -p1

%build
export CFLAGS="%optflags -L/usr/lib/firefox"
export LD=cc
libtoolize -f
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}
make

%install
export CFLAGS="-L/usr/lib/firefox -lxpcom"
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/gjs/*
%{_libdir}/gjs-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gjs-1.0/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%changelog
* Thu Oct 20 2011 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 0.30.0.
* Tue Jul 05 2011 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 0.7.14.
* Fri Oct 22 2010 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 0.7.4.
* Wed May 26 2010 - Erwann Cheneed <erwann.chenede@sun.com>
- Bumped to 0.7 + fix for 619721
* Tue Apr 27 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.6.
* Wed Mar 10 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.  Add BuildRequires SUNWprd.
* Sat Aug 29 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.4.
* Mon Aug 03 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Update to build with 0.3 tarball release.
* Tue Jul 07 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Add patch gjs-01-solaris.diff.
* Sat Apr 04 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
