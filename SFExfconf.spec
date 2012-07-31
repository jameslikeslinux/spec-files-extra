#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name xfconf
%define src_url http://archive.xfce.org/src/xfce/xfconf/4.8

Name:		SFExfconf
IPS_Package_Name:	xfce/config/xfce-config
Summary:	Configuration management for Xfce
Version:	4.8.1
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
License:	GPLv2
Group:		Desktop (GNOME)/Libraries
SUNW_Copyright:	xfconf.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SFExfce4-dev-tools
Requires:	SFExfce4-dev-tools
Requires:	SFElibxfce4util
BuildRequires:	SFElibxfce4util-devel
BuildRequires:	SUNWgtk-doc
BuildRequires:	SUNWgnome-xml-share

%package devel
Summary:	%{summary} - developer files
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
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
./configure --prefix=%{_prefix}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-gtk-doc		\
	--disable-visibility		\
	--disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete libtool .la files
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/xfce4
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1*

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libexecdir}/pkgconfig/*.pc
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Jan 17 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 4.8.1
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Sun Mar 20 2011 - Milan Jurik
- bump to 4.8.0, move to SFE from osol xfce
* Wed Aug 19 2009 - sobotkap@gmail.com
- Added IPS meta-tags required by juicer.
* Sat Feb 28 2009 - sobotkap@gmail.com
- Add xfconfd to packages files.
* Sun Dec 21 2008 - sobotkap@gmail.com
- Inital version.

