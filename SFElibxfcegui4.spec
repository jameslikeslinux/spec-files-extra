#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name libxfcegui4
%define src_url http://archive.xfce.org/src/xfce/libxfcegui4/4.8/

Name:		SFElibxfcegui4
Summary:	Various gtk widgets for xfce
License:	LGPLv2+
SUNW_Copyright:	libxfcegui4.copyright
Version:	4.8.1
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Group:		User Interface/Desktops
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:	SFExfce4-dev-tools
Requires:	SFElibxfce4util
BuildRequires:	SFElibxfce4util-devel
Requires:	SFExfconf
Requires:	SUNWgnome-ui-designer
BuildRequires:	SUNWgnome-ui-designer-devel
BuildRequires:	SUNWgnome-xml-share
BuildRequires:	SUNWgtk-doc

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

%files
%defattr(-, root, bin)
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, bin) %{_datadir}/glade3
%dir %attr (0755, root, bin) %{_datadir}/glade3/catalogs
%{_datadir}/glade3/catalogs/*
%dir %attr (0755, root, bin) %{_datadir}/glade3/pixmaps
%{_datadir}/glade3/pixmaps/*
%dir %attr (0755, root, bin) %{_libdir}/glade3/modules
%{_libdir}/glade3/modules/*

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%{_libdir}/libglade
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Jul 23 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Thu Apr 21 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 4.8.1
* Mon Mar 21 2011 - Milan Jurik
- bump to 4.8.0, move to SFE from osol xfce
* Fri Sep 24 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Remove all .la files.
* Tue Aug 03 2010 - brian.cameron@oracle.com
- Bump to 4.6.4.
* Mon Sep 21 2009 - sobotkap@gmail.com
- Add check if files for glade3 should be delivered or not.
* Wed Aug 19 2009 - sobotkap@gmail.com
- Added IPS meta-tags required by juicer.
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Wed Feb 21 2007 - Menno.Lageman@Sun.COM
- fix some gcc G_BEGIN_DECLS for Sun Studio build niceness
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
