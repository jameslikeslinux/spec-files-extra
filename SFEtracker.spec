#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define gnome_2_20  %(pkg-config --atleast-version=2.19.0 libgnome-2.0 && echo 1 || echo 0)

Name:           SFEtracker
License:        GPL
Summary:        Desktop search tool
Version:        0.6.3
URL:            http://www.tracker-project.org
Source:         http://www.gnome.org/~jamiemcc/tracker/tracker-%{version}.tar.bz2
Patch1:         tracker-01-w3m-crash.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:       SUNWgnome-base-libs
Requires:       SUNWdbus
Requires:       SUNWzlib
Requires:       SFEsqlite
Requires:       SFEgmime
Requires:       OSOLgamin
BuildRequires:  SUNWgnome-base-libs-devel
BuildRequires:  SUNWdbus-devel
BuildRequires:  SFEgmime-devel
BuildRequires:  SFEsqlite-devel
BUildRequires:  OSOLgamin-devel
#Additional recommended packages
Requires:       SUNWgnome-media
Requires:       SUNWpng
Requires:       SUNWogg-vorbis
Requires:       SUNWlibexif
Requires:       SUNWgnome-pdf-viewer
Requires:       SUNWlxsl
Requires:       SFEw3m
Requires:       SFEwv
Requires:       SFElibgsf
BuildRequires:  SUNWgnome-media-devel
BuildRequires:  SUNWpng-devel
BuildRequires:  SUNWogg-vorbis-devel
BuildRequires:  SUNWlibexif-devel
BuildRequires:  SUNWgnome-pdf-viewer-devel
BuildRequires:  SUNWlxsl-devel
BuildRequires:  SFEwv-devel
BuildRequires:  SFElibgsf-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n tracker-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

intltoolize --force --automake
./configure --prefix=%{_prefix} 		\
			--sysconfdir=%{_sysconfdir}	\
			--disable-warnings			\
			--enable-external-sqlite

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/tracker
%dir %attr (0755, root, bin) %{_libdir}/deskbar-applet
%if %gnome_2_20
%dir %attr (0755, root, bin) %{_libdir}/deskbar-applet/modules-2.20-compatible
%{_libdir}/deskbar-applet/modules-2.20-compatible/tracker-module.py
%else
%dir %attr (0755, root, bin) %{_libdir}/deskbar-applet/handlers
%{_libdir}/deskbar-applet/handlers/tracker-handler.py
%{_libdir}/deskbar-applet/handlers/tracker-handler-static.py
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/tracker
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/tracker.service
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%defattr (-, root, other)
%{_datadir}/icons

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Sep 26 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.3.
- Move wv and libgsf to Requires.
- Add patch w3m-crash to fix w3m crash on solaris.
* Fri Sep 21 2007 - trisk@acm.jhu.edu
- Fix install in GNOME 2.19/2.20
* Wed Sep 05 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.2.
- Move w3m to Requires.
* Thu Aug 09 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.1.
* Mon Aug 06 2007 - nonsea@users.sourceforge.net
- Add --enable-external-sqlite
* Fri Jul 24 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.0.
- Remove dependency on file.
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Add Requires to SFEsqlite
- Add conditional Requires to SFEwv
- Revert patch tracker-01-stdout.diff.
- Add attr (0755, root, other) to %{_datadir}/pixmaps
  and %{_datadir}/applications
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Add conditional Require SFElibgsf SFEw3m
- Remove upstreamed patch tracker-01-stdout.diff
- Add URL and License.
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Initial spec
