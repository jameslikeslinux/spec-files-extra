#
# spec file for package SFEtileworld
#
# includes module(s): tileworld
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use tileworld = tileworld.spec

Name:                    SFEtileworld
Summary:                 Tileworld - Chip's Challenge
Version:                 %{tileworld.version}
Group:                   Amusements/Games
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgtkmm-gpp
#Requires: SFElibmad
#Requires: SFEncurses
BuildRequires: SFEgtkmm-gpp
# TODO: more dependencies


%prep
rm -rf %name-%version
mkdir %name-%version
%tileworld.prep -d %name-%version


%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir} -lsocket -lnsl"
export CXXFLAGS="%gcc_cxx_optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%tileworld.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%tileworld.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/tworld/*
%{_mandir}/man6/*


%changelog
* Wed Dec 16 2011 - jchoi42@pha.jhu.edu
- initial spec
