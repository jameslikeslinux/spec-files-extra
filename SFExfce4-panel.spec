#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name xfce4-panel
#%define src_url http://archive.xfce.org/xfce/4.8/src/
%define src_url http://archive.xfce.org/src/xfce/xfce4-panel/4.8/

Name:		SFExfce4-panel
Summary:	Xfce Panel
Version:	4.8.5
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Group:		User Interface/Desktops
License:	GPLv2+
SUNW_Copyright: xfce4-panel.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:	SFExfce4-dev-tools
BuildRequires:	SFElibxfce4util-devel
Requires:	SFElibxfce4util
BuildRequires:	SFElibxfcegui4-devel
Requires:	SFElibxfcegui4
BuildRequires:	SFElibxfce4ui-devel
Requires:	SFElibxfce4ui
BuildRequires:	library/perl-5/xml-parser
Requires:	SFEgarcon
BuildRequires:	SFEgarcon-devel
Requires:	SFElibexo
BuildRequires:	SFElibexo-devel

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
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-gtk-doc		\
	--disable-static

make -j $CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete libtool .la files
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm $RPM_BUILD_ROOT%{_libdir}/xfce4/panel/plugins/*.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}
%{_libdir}/lib*.so*
%{_libdir}/xfce4*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_datadir}/gtk-doc*
%{_datadir}/xfce4*
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*

%files root
%defattr(-, root, sys)
%{_sysconfdir}

%files devel
%defattr(-,root,bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Aug 27 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 4.8.5
* Tue Aug 23 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 4.8.4
* Mon Jul 25 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Mon Apr 11 2011 - Milan Jurik
- GNU xgettext needed
* Wed Apr 9 2011 - kmays2000@gmail.com
- bump to 4.8.3
* Wed Mar 23 2011 - Milan Jurik
- bump to 4.8.0, move to SFE from osol xfce
* Tue Aug 03 2010 - brian.cameron@oracle.com
- Bump version to 4.6.4.
* Wed Aug 19 2009 - sobotkap@gmail.com
- Added IPS meta-tags required by juicer.
* Thu Aug 13 2009 - sobotkap@gmail.com
- Install to standart directories. Added include file xfce.inc.
* Sun Mar 01 2009 - sobotkap@gmail.com
- Use xfce prefixes, which allow to install to other directory then /usr
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
