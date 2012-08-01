#
# spec file for package SFEsigcpp-gpp
#
# includes module(s): libsigc++
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define _prefix %_basedir/g++

%use sigcpp = sigcpp.spec

Name:                    SFEsigcpp-gpp
IPS_Package_Name:	library/g++/sigcpp
Summary:                 Library that implements typesafe callback system for standard C++ (g++-built)
Group:                   Development/C++
URL:                     http://libsigc.sourceforge.net/
License:                 LGPLv2
SUNW_Copyright:          sigcpp.copyright
Version:                 %{sigcpp.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SFEgccruntime
Requires: SFEgccruntime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%sigcpp.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%cxx_optflags"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
%sigcpp.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%sigcpp.install -d %name-%version
rm $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%_includedir
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/sigc++*
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/doc
%_datadir/doc/%{sigcpp.name}-%{sigcpp.major_minor}
%_datadir/devhelp

%changelog
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout; add SUNW_Copyright
* Thu Jun 26 2008 - river@wikimedia.org
- need to use SFW gcc, not SFE because flags depend on Sun ld
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWsigcpp.spec to build with g++
