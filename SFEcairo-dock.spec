#
# spec file for package SFEcairo-dock
# Mon premier package, soyez indulgent...
# Gilles Dauphin
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define	src_name	cairo-dock
%define ver_major	2.3.0
%define ver_minor	3

Name:		SFEcairo-dock
IPS_Package_Name:	desktop/dock/cairo-dock
Summary:	A dock, providing a GUI for the launching of applications and other actions
Version:	%{ver_major}.%{ver_minor}
Group:		Applications/Panels and Applets
License:        GPLv3+
SUNW_Copyright: cairo-dock.copyright
Source:		http://launchpad.net/%{src_name}-core/2.3/%{ver_major}/+download/%{src_name}-%{ver_major}~%{ver_minor}.tar.gz
URL:		glx-dock.org
Patch1:		cairo-dock-01-cmake.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
Requires: 	SUNWpng
Requires: 	SUNWdbus
Requires: 	SUNWgnome-base-libs
Requires: 	SUNWgnome-wm
BuildRequires: 	SUNWpng-devel
BuildRequires: 	SUNWdbus-devel
BuildRequires: 	SUNWgnome-base-libs-devel
BuildRequires: 	SUNWgnome-wm-devel
BuildRequires: 	SUNWcompiz
Requires:	SFEgtkglext
BuildRequires:	SFEgtkglext-devel
BuildRequires:	SFEcmake


%package devel
Summary:		 %summary - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -n %{src_name}-%{ver_major}~%{ver_minor}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
export CC=gcc
export CXX=g++

mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr

make -j$CPUS

%install
rm -rf %{buildroot}

cd build
make install DESTDIR=%{buildroot}

%if %build_l10n
%else
rm -rf %{buildroot}%{_datadir}/locale
%endif


%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}/*.so*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/cairo-dock
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Wed Jul 13 2011 - Milan Jurik
- update to 2.3.0-3
* Mon Feb 21 2011 - Milan Jurik
- update to 2.2.0-4
* Aug 04 2009 - Gilles Dauphin ( Gilles POINT Dauphin A enst POINT fr)
- require CBEgettext , SUNWgnu-gettext is not enough.
* April 22 2008 - Gilles Dauphin ( Gilles POINT Dauphin A enst POINT fr)
- Initial spec
