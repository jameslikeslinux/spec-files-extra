#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name xfce4-session
#%define src_url http://archive.xfce.org/xfce/4.8/src/
%define src_url http://archive.xfce.org/src/xfce/xfce4-session/4.8/

Name:		SFExfce4-session
Summary:	Xfce Session manager
Version:	4.8.2
URL:		http://www.xfce.org/
License:	GPLv2
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		xfce4-session-01-rbac.diff
Group:		User Interface/Desktops
SUNW_Copyright:	xfce4-session.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-config 
BuildRequires: SUNWgnome-panel 
BuildRequires: SUNWlibatk 
BuildRequires: SUNWcairo 
BuildRequires: SUNWgtk2 
BuildRequires: SFElibxfce4util 
BuildRequires: SUNWpango 
BuildRequires: SUNWglib2 
BuildRequires: SUNWlibgnome-keyring 
BuildRequires: SUNWfontconfig
BuildRequires: SUNWfreetype2 
BuildRequires: SUNWdbus-libs
BuildRequires: SUNWdbus-glib 
BuildRequires: SUNWlibms 
BuildRequires: SUNWxwice 
Requires: SUNWgnome-config 
Requires: SUNWgnome-panel 
Requires: SUNWlibatk 
Requires: SUNWcairo 
Requires: SUNWgtk2 
Requires: SFElibxfce4util 
Requires: SUNWpango 
Requires: SUNWglib2 
Requires: SUNWlibgnome-keyring 
Requires: SUNWfontconfig
Requires: SUNWfreetype2 
Requires: SUNWdbus-libs
Requires: SUNWdbus-glib 
Requires: SUNWlibms 
Requires: SUNWxwice 
BuildRequires:	SFExfce4-dev-tools
BuildRequires:	SFElibxfcegui4-devel
Requires:	SFElibxfcegui4
BuildRequires:	SFElibxfce4ui-devel
Requires:	SFElibxfce4ui
BuildRequires:	SFExfce4-panel-devel
Requires:	SFExfce4-panel
Requires:	SFExfconf
Requires:	SUNWpostrun

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%package devel
Summary:	%{summary} - developer files
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export ICEAUTH=/usr/openwin/bin/iceauth
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -lsecdb -lsocket -lnsl"
# GNU xgettext needed
export PATH=/usr/gnu/bin:$PATH
./configure --prefix=%{_prefix}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-gnome			\
	--enable-libgnome-keyring	\
	--disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete libtool .la files
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr(-,root,bin)
%{_bindir}
%{_libdir}/lib*.so*
%{_libdir}/xfce4*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/xfce4*
%{_datadir}/themes*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64/apps
%{_datadir}/icons/hicolor/64x64/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/72x72
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/72x72/apps
%{_datadir}/icons/hicolor/72x72/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128/apps
%{_datadir}/icons/hicolor/128x128/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%files root
%defattr(-,root,sys)
%{_sysconfdir}

%files devel
%defattr(-,root,bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 4.8.2
* Tue Aug 23 2011 - Ken Mays <kmays2000@gmail.com>
- Added required dependencies for other build systemss
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Mon Apr 11 2011 - Milan Jurik
- GNU xgettext needed
* Thu Apr 9 2011 - kmays2000@gmail.com
- bump to 4.8.1
* Thu Mar 24 2011 - Milan Jurik
- bump to 4.8.0, move to SFE from osol xfce
* Wed Aug 19 2009 - sobotkap@gmail.com
- Fix source repository url
* Sat Aug 15 2009 - sobotkap@gmail.com
- Bumped to version 4.6.1
* Mon Dec 10 2007 - sobotkap@centrum.cz
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
