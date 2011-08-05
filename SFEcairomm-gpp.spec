#
# spec file for package SFEcairomm-gpp
#
# includes module(s): cairomm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define _basedir /usr/g++

%use cairomm = cairomm.spec

Name:                    SFEcairomm-gpp
Summary:                 C++ API for the Cairo Graphics Library (g++-built)
Group:                   Desktop (GNOME)/Libraries
License:                 LGPLv2
SUNW_Copyright:          cairomm.copyright
Version:                 %{cairomm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp-gpp
BuildRequires: SFEsigcpp-gpp-devel
BuildRequires: SUNWsigcpp-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SUNWsigcpp-devel
Requires: SFEsigcpp-gpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%cairomm.prep -d %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
#export CPPFLAGS="-I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export CFLAGS="%optflags"
export PERL_PATH=/usr/perl5/bin/perl
export LDFLAGS="-L/usr/gnu/lib:/usr/g++/lib -R/usr/gnu/lib -R/usr/g++/lib"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
%cairomm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%cairomm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# delete files already included in SUNWcairomm-devel:
#rm -r $RPM_BUILD_ROOT%{_datadir}
#rm -r $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%_libdir/cairomm-1.0
%_includedir
%_datadir/doc/cairomm-1.0
%_datadir/devhelp

%changelog
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout add SUNW_Copyright
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWcairomm.spec to build with g++
