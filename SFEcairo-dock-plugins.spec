#
# spec file for package SFEcairo-dock-plugins
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# NOTE: -Denable_alsa_mixer="no" does not seem to work at the moment, so
#	you must ensure that Alsa is not installed to get this to build.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define	src_name	cairo-dock-plugins
%define ver_major	2.3.0
%define ver_minor	3

%define SUNWlibxklavier %(/usr/bin/pkginfo -q SUNWlibxklavier && echo 1 || echo 0)

Name:           SFEcairo-dock-plugins
Summary:        cairo-dock plugins
Version:        %{ver_major}.%{ver_minor}
License:        GPLv3+ and LGPLv2+
SUNW_Copyright: cairo-dock-plugins.copyright
Source:		http://launchpad.net/cairo-dock-plug-ins/2.3/%{ver_major}/+download/%{src_name}-%{ver_major}~%{ver_minor}.tar.gz
Patch1:		cairo-dock-plugins-01-cmake.diff
Patch2:		cairo-dock-plugins-02-solaris.diff
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
BuildRequires:	SFEcmake
Requires:	SFEcairo-dock
BuildRequires:	SFEcairo-dock-devel
Requires:	SFEgtkglext
BuildRequires:	SFEgtkglext-devel
%if %SUNWlibxklavier
Requires:	SUNWlibxklavier
BuildRequires:	SUNWlibxklavier-devel
%endif
Requires:	SFElibetpan
BuildRequires:	SFElibetpan-devel
Requires:	SUNWlibexif
BuildRequires:	SUNWlibexif-devel
Requires:	SUNWvala
BuildRequires:	SUNWvala-devel
Requires:	SFEwebkitgtk
BuildRequires:	SFEwebkitgtk-devel


%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{ver_major}~%{ver_minor}
%patch1 -p1
%patch2 -p1

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
cmake .. -DCMAKE_INSTALL_PREFIX=/usr -Denable_alsa_mixer="no"

#make -j$CPUS
make VERBOSE=1

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
%{_libdir}
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/cairo-dock
#%{_datadir}/vala-0.10

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Jul 27 2011 - Alex Viskovatoff
- don't package %{_datadir}/vala-0.10, which no longer gets created
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Wed Jul 13 2011 - Milan Jurik
- update to 2.3.0-3
* Wed May 11 2011 - Alex Viskovatoff
- Disable alsa-mixer plugin, which breaks the build
* Mon Feb 21 2011 - Milan Jurik
- Initial spec
