#
# spec file for package SFElibgmtk
#
# Copyright 2012 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define _prefix /usr/g++

Name:		SFElibgmtk
IPS_package_name: library/desktop/g++/libgmtk
Summary:	GMTK - Gnome-Mplayer Toolkit
Group:		Desktop (GNOME)/Libraries
Version:	1.0.5
License:	GPL
Source:		http://gmtk.googlecode.com/files/gmtk-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc

BuildRequires:	SFEgettext-devel
Requires:	SFEgettext
BuildRequires:	SFEgtkmm-gpp-devel
Requires:	SFEgtkmm-gpp


%prep
%setup -q -n gmtk-%version


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export PATH=/usr/g++/bin:/usr/gnu/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib"
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir}
gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%_includedir
%dir %attr (-, root, sys) %_datadir
%{_datadir}/locale/*
%dir %attr (0755, root, other) %dir %_docdir
%_datadir/doc/gmtk


%changelog
* Wed Jan 25 2012 - James Choi
- Initial spec
