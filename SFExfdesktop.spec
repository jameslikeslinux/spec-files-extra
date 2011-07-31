#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name xfdesktop
#%define src_url http://archive.xfce.org/xfce/4.8/src/
%define src_url http://archive.xfce.org/src/xfce/xfdesktop/4.8/

Name:		SFExfdesktop
Summary:	Desktop manager for the Xfce Desktop Environment
Version:	4.8.1
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
License: 	GPLv2
Group:		User Interface/Desktops
SUNW_Copyright: xfdesktop4.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:	SFExfce4-dev-tools
BuildRequires:	SFElibxfcegui4-devel
Requires:	SFElibxfcegui4
BuildRequires:	SFElibxfce4ui-devel
Requires:	SFElibxfce4ui
Requires:	SFExfconf
BuildRequires:	SFEthunar-devel
Requires:	SFEthunar

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
	--bindir=%{_bindir}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/xfce4
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Mon Apr 11 2011 - Milan Jurik
- GNU xgettext needed
* Thu Apr 9 2011 - kmays2000@gmail.com
- bump to 4.8.1
* Fri Mar 25 2011 - Milan Jurik
- bump to 4.8.0, move to SFE from osol xfce
* Fri Sep 24 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Remove all .la files.
* Sun Aug 16 2009 - sobotkap@gmail.com
- Modify files section for version 4.6.1
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
