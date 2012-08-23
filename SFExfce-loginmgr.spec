#
# Copyright (c) 2011 Oracle Corporation
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include xfce.inc
#include base.inc

%define src_name        xfce-loginmgr

Name:			SFExfce-loginmgr
Summary:		gdm and dtlogin files to support Xfce
IPS_package_name:	xfce/xfce-loginmgr
URL:			http://www.opensolaris.org/
Version:		%{xfce_version}
Source0:		Xinitrc.xfce
Source1:		Xsession.xfce
Source2:		Xsession2.xfce
Source3:		Xresources.xfce
Source4:		xfce.desktop
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/dt/config/C/Xresources.d
cp %{SOURCE0} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE1} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE2} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE3} $RPM_BUILD_ROOT/usr/dt/config/C/Xresources.d
mkdir -p $RPM_BUILD_ROOT/usr/share/xsessions
cp %{SOURCE4} $RPM_BUILD_ROOT/usr/share/xsessions

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) /usr/dt
%dir %attr (0755, root, bin) /usr/dt/config
%dir %attr (0755, root, bin) /usr/dt/config/C
%dir %attr (0755, root, bin) /usr/dt/config/C/Xresources.d
/usr/dt/config/C/Xresources.d/*
%attr (0755, root, bin) /usr/dt/config/Xinitrc.xfce
%attr (0755, root, bin) /usr/dt/config/Xsession.xfce
%attr (0755, root, bin) /usr/dt/config/Xsession2.xfce
%{_datadir}/*

%changelog
* Mon Oct 17 2011 - Ken Mays <kmays2000@gmail.com>
- Migrated from OSOL to SFE.
* Wed Aug 04 2010 - brian.cameron@oracle.com
- Fix includes.
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Fri Feb  9 2007 - dougs@truemail.co.th
- Changed from tar archives to normal files
- Changed startup script in xfce.desktop from Xinitrc.xfce to Xsession.xfce
* Thu Feb  2 2007 - dougs@truemail.co.th
- Initial version
