#
# spec file for package SFElightdm
#
# includes module(s): lightdm
#
# bugdb: bugzilla.freedesktop.org
#

%include Solaris.inc
Name:                    SFElightdm
License:                 GPLv3
SUNW_Copyright:	         lightdm.copyright
Version:                 0.9.2
Source:                  http://launchpad.net/lightdm/trunk/%{version}/+download/lightdm-%{version}.tar.gz
Source1:                 lightdm.xml
Source2:                 svc-lightdm
Patch1:                  lightdm-01-compile.diff
Patch2:                  lightdm-02-vala.diff
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 Light Display Manager
URL:                     https://launchpad.net/~lightdm-team/+archive/ppa
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}

%description

LightDM is a cross-desktop display manager that aims to be the standard display
manager for the X.org X server. The motivation for this project is there have
been many new display managers written since XDM (often based on the XDM
source). The main difference between these projects is in the GUIs (e.g.
different toolkits) and performance - this could be better accomplished with a
common display manager that allows these differences.

Key features are:

A well-defined greeter API allowing multiple GUIs
Support for all display manager use cases, with plugins where appropriate
Low code complexity
Fast performance 

%include default-depend.inc
Requires:                SUNWglib2
Requires:                SUNWgtk2
Requires:                SUNWconsolekit
Requires:                SUNWdbus-glib
Requires:                SUNWlibxklavier
#Requires:                SFEwebkitgtk
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SUNWlibxklavier-devel
#BuildRequires:           SFEwebkitgtk-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -q -n lightdm-%version
%patch1 -p1
%patch2 -p1

%build
libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf
./configure \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --sysconfdir=%{_sysconfdir}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

install -d $RPM_BUILD_ROOT/lib/svc/manifest/application/graphical-login
install --mode=0444 %SOURCE1 $RPM_BUILD_ROOT/lib/svc/manifest/application/graphical-login
install -d $RPM_BUILD_ROOT/lib/svc/method
cp %SOURCE2 $RPM_BUILD_ROOT/lib/svc/method/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%attr (0755, root, bin)%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir-1.0/*
%{_datadir}/gtk-doc/*
%{_datadir}/vala
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/lightdm.1

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/*
%{_sysconfdir}/init/lightdm.conf
%{_sysconfdir}/lightdm
# SVC method file
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%dir %attr (0755, root, sys) /lib/svc/manifest
%dir %attr (0755, root, sys) /lib/svc/manifest/application
%dir %attr (0755, root, sys) /lib/svc/manifest/application/graphical-login
%attr (0555, root, bin) /lib/svc/method/svc-lightdm
%attr (0444, root, sys) /lib/svc/manifest/application/graphical-login/lightdm.xml

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Jul 23 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Tue Jul 19 2011 - Brian Cameron  <brian.cameron@oracle.com>
- Bump to 0.4.4.
* Fri May 20 2011 - Brian Cameron  <brian.cameron@oracle.com>
- Bump to 0.3.4.  Rework patches.
* Sat Oct 09 2010 - Simon Jin      <yun-tong.jin@oracle.com>
- Bump to 0.1.2, reorder the patches.
* Thu Aug 26 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Created with version 0.1.1.
