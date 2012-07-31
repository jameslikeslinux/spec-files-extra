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

%use gtksourceviewmm = gtksourceviewmm.spec

Name:                    SFEgtksourceviewmm-gpp
Summary:                 %{gtksourceviewmm.summary} (g++-built)
URL:                     %{gtksourceviewmm.url}
Group:                   Desktop (GNOME)/Libraries
License:                 LGPLv2
#SUNW_Copyright:          gtksourceviewmm.copyright
Version:                 %{gtksourceviewmm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEgtkmm-gpp
BuildRequires: SFEgtkmm-gpp-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%gtksourceviewmm.prep -d %name-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
#export CPPFLAGS="-I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export CFLAGS="%optflags"
export PERL_PATH=/usr/perl5/bin/perl
export LDFLAGS="-L/usr/g++/lib:/usr/gnu/lib -R/usr/g++/lib:/usr/gnu/lib"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
%gtksourceviewmm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gtksourceviewmm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%_libdir/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/*
%_libdir/gtksourceviewmm-2.0
%_includedir
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %dir %_docdir
%_datadir/doc/gtksourceviewmm-2.0
%_datadir/devhelp

%changelog
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout add SUNW_Copyright
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWcairomm.spec to build with g++
