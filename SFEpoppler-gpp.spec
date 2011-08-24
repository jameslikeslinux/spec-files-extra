#
# spec file for package SFEpoppler-gpp
#
# includes module(s): poppler
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define _prefix /usr/g++

%use poppler = poppler.spec

Name:                    SFEpoppler-gpp
Summary:                 PDF rendering library (g++-built)
URL:                     http://poppler.freedesktop.org
License:                 GPLv2
SUNW_Copyright:          poppler.copyright
Version:                 %{poppler.version}
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
Requires: SFEsigcpp-gpp-devel
Requires: SUNWsigcpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%poppler.prep -d %name-%version

%build
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CXXFLAGS="%cxx_optflags -fpermissive"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
export LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib"
export PERL_PATH=/usr/perl5/bin/perl
%poppler.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%poppler.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# RUNPATH ends up getting incorrectly set, with /usr/g++/lib behind /usr/lib
%define rpath 'dyn:runpath /usr/g++/lib:/usr/gnu/lib'
pushd %buildroot%_libdir
elfedit -e %rpath libpoppler-cpp.so.0.1.0
elfedit -e %rpath libpoppler-glib.so.5.0.0
elfedit -e %rpath libpoppler.so.7.0.0
popd

# REMOVE l10n FILES - included in Solaris
#rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

# remove files included in SUNWgnome-pdf-viewer[-devel]:
rm -r $RPM_BUILD_ROOT%{_mandir}
#rm -r $RPM_BUILD_ROOT%{_includedir}
rm -r $RPM_BUILD_ROOT%{_bindir}

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
%_includedir
%dir %attr (0755, root, sys) %{_datadir}
%_datadir/gtk-doc

%changelog
* Fri Aug  5 2011 - Alex Viskovatoff
- use new g++ path layout; add SUNW_Copyright
* Wed Apr 23 2008 - laca@sun.com
- create
