#
# spec file for package SFEglibmm-gpp
#
# includes module(s): glibmm
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define _prefix /usr/g++

%use glibmm = glibmm.spec

Name:                    SFEglibmm-gpp
Summary:                 C++ Wrapper for the Glib2 Library (g++-built)
Group:                   Desktop (GNOME)/Libraries
License:                 LGPLv2
SUNW_Copyright:          glibmm.copyright
Version:                 %{glibmm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp-gpp
BuildRequires: SFEsigcpp-gpp-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp-gpp-devel
Requires: SUNWsigcpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%glibmm.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CXXFLAGS="%{cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig
export LDFLAGS="-L/usr/gnu/lib:/usr/g++/lib -R/usr/gnu/lib -R/usr/g++/lib"
export PERL_PATH=/usr/perl5/bin/perl
%glibmm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%glibmm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Remove useless m4, pm and extra_gen_defs files 
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/glibmm-2.4/proc/m4
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/glibmm-2.4/proc/pm
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/libglibmm_generate_extra_defs*.so*
rm -rf $RPM_BUILD_ROOT%{_cxx_includedir}/glibmm-2.4/glibmm_generate_extra_defs
rm -rf $RPM_BUILD_ROOT%_datadir/aclocal

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
%{_libdir}/glibmm*
%{_libdir}/giomm*
%_datadir/doc/glibmm-2.4
%_datadir/glibmm-2.4
%_datadir/devhelp

%changelog
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout; add SUNW_Copyright
* Fri Nov 06 2009 - jchoi42@pha.jhu.edu
- comment deprecated patch
* Fri Sep 25 2009 - jchoi42@pha.jhu.edu
- specified giomm dir in %files section
* Sun Jun 29 2008 - river@wikimedia.org
- force to use gcc in /usr/sfw, not /usr/gnu
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWglibmm.spec to build with g++
