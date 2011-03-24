#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name xfce4-settings
%define src_url http://archive.xfce.org/xfce/4.8/src/

Name:		SFExfce4-settings
Summary:	Various gtk widgets for xfce
Version:	4.8.0
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Group:		User Interface/Desktops
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:	SUNWgnome-common-devel
BuildRequires:	SFExfce4-dev-tools
Requires:	SFElibxfce4util
BuildRequires:	SFElibxfce4util-devel
Requires:	SFElibexo
BuildRequires:	SFElibexo-devel

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

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
./configure --prefix=%{_prefix}		\
	--libdir=%{_libdir}		\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-pluggable-dialogs	\
	--enable-sound-settings		\
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

%files
%defattr(-,root,bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%files root
%attr (0755, root, sys) %dir %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/*
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/autostart
%{_sysconfdir}/xdg/autostart/*
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/xfce4
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/xfce4/xfconf
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Mar 24 2011 - Milan Jurik
- bump to 4.8.0, move to SFE from osol xfce
* Fri Jan 21 2011  Brian Cameron  <brian.cameron@oracle.com>
- Add requires on OSOLlibexo.
* Sat 15 2009  Petr Sobotka   sobotkap@gmail.com
- Initial version
