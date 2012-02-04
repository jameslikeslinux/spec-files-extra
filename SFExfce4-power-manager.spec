#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name xfce4-power-manager
%define src_url http://archive.xfce.org/src/xfce/xfce4-power-manager/1.0/

Name:		SFExfce4-power-manager
IPS_Package_Name:	xfce/xfce-power-manager
Summary:	Xfce Power management utilities
Version:	1.0.10
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
License:	GPLv2
Patch1:		xfce4-power-manager-01-solaris-diff
Group:		Applications/System Utilities
SUNW_Copyright:	xfce4-power-manager.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:  SUNWdbus
BuildRequires:	SFExfce4-panel-devel
Requires:	SFExfce4-panel
BuildRequires:	SFElibxfce4ui
BuildRequires:  SFElibxfce4util
Requires:	SFExfce4-panel
BuildRequires:  SFExfconf
Requires:	%{name}-root

%description
xfce4-power-manager is a tool for the Xfce desktop environment for managing profiles of policies which affect power consumption, such as the display brightness level, display sleep times, or CPU frequency scaling. It can also trigger actions on certain events such as closing the lid or reaching low battery levels and provides a set of interfaces to inform other applications about current power level so that they can adjust their power consumption. Furthermore, it provides the a standardized inhibit interface which allows applications to prevent automatic sleep actions via the power manager. 

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
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

# GNU xgettext needed
export PATH=/usr/gnu/bin:$PATH
./configure --prefix=%{_prefix}		\
	--bindir=%{_bindir}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}

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
%defattr(-, root, bin) 
%doc AUTHORS COPYING ChangeLog NEWS README TODO 
%{_bindir} 
%{_libdir}/xfce4/panel-plugins
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}
%{_datadir}/polkit-1 
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/xfce4-power-manager-settings.desktop 
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/actions
%{_datadir}/icons/hicolor/16x16/actions/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/status
%{_datadir}/icons/hicolor/16x16/status/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/actions
%{_datadir}/icons/hicolor/22x22/actions/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/status
%{_datadir}/icons/hicolor/22x22/status/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/actions
%{_datadir}/icons/hicolor/24x24/actions/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/status
%{_datadir}/icons/hicolor/24x24/status/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/actions
%{_datadir}/icons/hicolor/48x48/actions/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/status
%{_datadir}/icons/hicolor/48x48/status/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/devices
%{_datadir}/icons/hicolor/128x128/devices/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/actions
%{_datadir}/icons/hicolor/scalable/actions/* 
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/status
%{_datadir}/icons/hicolor/scalable/status/* 
%doc %{_datadir}/xfce4/doc 
%{_datadir}/xfce4/panel-plugins
%{_sbindir}

%files root
%defattr(-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/autostart
%config %{_sysconfdir}/xdg/autostart/xfce4-power-manager.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Thu Apr 21 2011 - Ken Mays <kmays2000@gmail.com
- Initial spec for 1.0.10
