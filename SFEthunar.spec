#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name Thunar
#%define src_url http://archive.xfce.org/xfce/4.8/src/
%define src_url http://archive.xfce.org/src/xfce/thunar/1.3/

Name:		SFEthunar
Summary:	Thunar File Manager
Version:	1.3.0
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
License:	GPLv2
SUNW_Copyright:	thunar.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:	SFExfce4-dev-tools
Requires:	SFElibexo
BuildRequires:	SFElibexo-devel
Requires:	SFExfce4-panel
BuildRequires:	SFExfce4-panel-devel
Requires:	SUNWgamin
BuildRequires:	SUNWgamin-devel
Requires:	SUNWlibexif
BuildRequires:	SUNWlibexif-devel
Requires:	SUNWpcre
BuildRequires:	SUNWpcre

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

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
# GNU xgettext needed
export PATH=/usr/gnu/bin:$PATH
./configure --prefix=%{_prefix}		\
	--sbindir=%{_sbindir}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-gtk-doc		\
	--enable-dbus			\
	--disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete libtool .la files
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm $RPM_BUILD_ROOT%{_libdir}/thunarx-2/*.la

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
%{_libdir}/xfce4
%{_libdir}/thunarx-2
%{_libdir}/Thunar
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_datadir}/xfce4
%{_datadir}/dbus-1
%{_datadir}/Thunar
%{_datadir}/gtk-doc
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/stock
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/stock/navigation
%{_datadir}/icons/hicolor/16x16/stock/navigation/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/stock
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/stock/navigation
%{_datadir}/icons/hicolor/24x24/stock/navigation/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (-, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%files root
%defattr(-,root,sys)
%{_sysconfdir}

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_includedir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Mon Apr 11 2011 - Milan Jurik
- GNU xgettext needed
* Sat Apr 9 2011 - kmays2000@gmail.com
- bump to 1.3.0
* Thu Mar 24 2011 - Milan Jurik
- bump to 1.2.0, move to SFE from osol xfce
* Fri Aug 14 2009 - sobotkap@gmail.com
- Added include file xfce.inc for useful Xfce marcros.
* Sun Dec  9 2007 - sobotkap@centrum.cz
- Bumped to 0.9.0
* Sun Apr 15 2007 - dougs@truemail.co.th
- Added OSOLgamin as a required package
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Feb  9 2007 - dougs@truemail.co.th
- Added SUNWpcre requirement
* Thu Feb  2 2007 - dougs@truemail.co.th
- Initial version
