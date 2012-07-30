#
# spec file for package SFEsparsehash
#
# includes module(s): sparsehash
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define _prefix /usr/g++

%use sparsehash = sparsehash.spec

Name:                    SFEsparsehash
IPS_Package_Name:	 library/desktop/g++/sparsehash
Summary:                 An extremely memory-efficient hash_map implementation
Group:                   Desktop (GNOME)/Libraries
License:                 BSD    
Version:                 %{sparsehash.version}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgccruntime
#BuildRequires: SFEsigcpp-gpp
#BuildRequires: SFEsigcpp-gpp-devel


%prep
rm -rf %name-%version
mkdir %name-%version
%sparsehash.prep -d %name-%version

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib"
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
%sparsehash.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%sparsehash.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %dir %{_docdir}
%{_datadir}/doc/sparsehash-%version


%changelog
* Fri Jan 13 2012 - James Choi
- Initial spec
