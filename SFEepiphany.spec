#
# spec file for package SFEepiphany
#
# includes module(s): epiphany
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include Solaris.inc

%use epiphany = epiphany.spec

%define revision = %{epiphany.revision}

Name:                    SFEepiphany
IPS_Package_Name:	web/browser/epiphany
Summary:                 GNOME web browser - epiphany
Version:                 %{epiphany.version}
URL:		%{epiphany.url}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWfirefox
Requires: SUNWdbus
Requires: SUNWlibmsr
Requires: SUNWprd
Requires: SFEwebkitgtk
Requires: SUNWgnome-gvfs
Requires: SFEgconfmm
Requires: SFEseed
Requires: SUNWgobject-introspection
Requires: SUNWavahi-bridge-dsd
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWfirefox-devel
BuildRequires: SUNWprd
BuildRequires: SFEwebkitgtk-devel
BuildRequires: SFEgconfmm-devel
BuildRequires: SFEseed-devel
BuildRequires: SUNWgobject-introspection-devel
BuildRequires: SUNWtlsd
BuildRequires: SUNWavahi-bridge-dsd-devel

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

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
rm -rf %name-%version
mkdir %name-%version
%epiphany.prep -d %name-%version

%build
%epiphany.build -d %name-%version

%install
rm -rf %{buildroot}
%epiphany.install -d %name-%version

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf %{buildroot}%{_datadir}/locale
%endif

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/epiphany
%{_datadir}/epiphany/*
%dir %attr (-, root, bin) %{_datadir}/dbus-1
%{_datadir}/dbus-1/*
%dir %attr (-, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%dir %attr (-, root, other) %{_datadir}/icons
#%{_datadir}/icons/*
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
%dir %attr (-, root, other) %{_datadir}/icons/LowContrastLargePrint
%dir %attr (-, root, other) %{_datadir}/icons/LowContrastLargePrint/48x48
%dir %attr (-, root, other) %{_datadir}/icons/LowContrastLargePrint/48x48/apps
%{_datadir}/icons/LowContrastLargePrint/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrint
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrint/48x48
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrint/48x48/apps
%{_datadir}/icons/HighContrastLargePrint/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrintInverse
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrintInverse/48x48
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrintInverse/48x48/apps
%{_datadir}/icons/HighContrastLargePrintInverse/48x48/apps/*
%{_libdir}/girepository-1.0
%{_datadir}/gir-1.0

%files devel
%defattr (-, root, bin)
%{_includedir}/epiphany
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%{_datadir}/omf
%{_mandir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/epiphany*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Nov 20 2011 - Milan Jurik
- bump to 2.30.6, add javascript
* Fri Feb 12 2010 - jchoi42@pha.jhu.edu
- add devel pkg
- update %files for new filenames, add %revision, remove gvfs module
- add dependencies to gvfs, webkit, update install to gpp-built libdir 
* Thu Nov 07 2007 - damien.carbery@sun.com
- Initial version.
