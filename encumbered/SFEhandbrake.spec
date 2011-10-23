#
# spec file for package SFEhandbrake
#
# includes module(s): handbrake
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%use handbrake = handbrake.spec

Name:                    SFEhandbrake
IPS_Package_Name:	video/handbrake
Summary:                 handbrake - multiplatform, multithreaded video transcoder
URL:		http://handbrake.fr/
Version:                 %{handbrake.version}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgcc
Requires: SFEfaad2
Requires: SFElibx264
Requires: SFElibmad
Requires: SFElibao
Requires: SFExvid
Requires: SFEffmpeg
Requires: SFElibmp4v2
Requires: SFElibdvdnav
Requires: SFElibiconv
Requires: SFElibschroedinger
BuildRequires: SFEgcc
BuildRequires: SFEffmpeg-devel
BuildRequires: SFElibx264-devel
BuildRequires: SFElibao-devel
BuildRequires: SFElibiconv-devel
BuildRequires: SFEyasm

Requires:       %{pnm_requires_SUNWlibmikmod}
BuildRequires:  %{pnm_buildrequires_SUNWlibmikmod}

BuildRequires:	SUNWaudh

# TODO: more dependencies?



%prep
rm -rf %name-%version
mkdir %name-%version
%handbrake.prep -d %name-%version

%build
export CC='gcc'
export CXX=g++
export CFLAGS="%gcc_optflags -Os -Xlinker -i"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir} -lsocket -lnsl -liconv %_ldflags %{xorg_lib_path} -L/usr/gnu/lib -R/usr/gnu/lib -L%{_libdir} -R%{_libdir} -m64"
export CXXFLAGS="%gcc_cxx_optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%handbrake.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%handbrake.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
#%{_bindir}/HandBrakeCLI
%{_bindir}/*
#%{_bindir}/somecrap


%changelog
* Thu Feb 25 2011 - jchoi42@pha.jhu.edu
- migrate SFE/SUNW detection to packagenamemacros.inc format
* Sat Feb 05 2011 - jchoi42@pha.jhu.edu
- fix dependencies, fix ldflags, add smart libmikmod detection
* Wed Dec 16 2010 - jchoi42@pha.jhu.edu
- initial spec
