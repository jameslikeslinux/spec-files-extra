#
# spec file for package SFEpythia8
#
# includes module(s): pythia8
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define _prefix /usr/g++

%use pythia8 = pythia8.spec

Name:                    SFEpythia8
IPS_Package_Name:	 library/desktop/g++/pythia8
Summary:                 Pythia - event generator for large physics processes
Group:                   Math
License:                 GPL
Version:                 %{pythia8.version}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Requires: SFEgcc
#BuildRequires: SFEsigcpp-gpp-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name


%description
With the release of PYTHIA 8.100, this new C++ version series takes 
over from the older Fortran 77-based PYTHIA 6.4 one as the current 
standard. It is strongly recommended to use PYTHIA 8.1 for LHC studies, 
although it has maybe not yet been tested and tuned enough to offer a 
complete replacement for major production runs. Nevertheless it does by 
now offer many features not found in PYTHIA 6.4, which should make a 
rapid transition worthwhile.

The current release is focused towards LHC and Tevatron applications, 
i.e. high-energy pp and pbarp collisions. Also e+e- and mu+mu- 
annihilation processes may be simulated, but not e.g. ep, gammap or 
gammagamma collisions. This is the major example where PYTHIA 6.4 still 
has more to offer.


%prep
rm -rf %name-%version
mkdir %name-%version
%pythia8.prep -d %name-%version

%build
export CC=gcc
export CXX=g++
export USRCXXFLAGS="-fPIC"
export PYTHIA8DATA=%{_docdir}/pythia-{majorversion}/xmldoc
%pythia8.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%pythia8.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_includedir}/pythia-%{pythia8.majorversion}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %dir %{_docdir}
%{_datadir}/doc/pythia-%{pythia8.majorversion}/htmldoc
%{_datadir}/doc/pythia-%{pythia8.majorversion}/phpdoc
%{_datadir}/doc/pythia-%{pythia8.majorversion}/xmldoc



%changelog
* Fri Jan 13 2012 - James Choi
- Initial spec
