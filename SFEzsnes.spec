#
# spec file for package SFEzsnes
#
# includes module(s): zsnes
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use zsnes = zsnes.spec

Name:                    SFEzsnes
Summary:                 ZSNES - Super Nintendo emulator
Version:                 %{zsnes.version}
Group:                   Amusements/Games
SUNW_BaseDir:            %{_basedir}
Patch1:                  zsnes-01-devnull.diff
Patch2:                  zsnes-02-solaris.diff
Patch3:                  zsnes-03-naming.diff

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEglibmm-gpp
Requires: SFEgtkmm-gpp
#Requires: SFElibmad
#Requires: SFElibao
BuildRequires: SFEgtkmm-gpp

# TODO: more dependencies?

%prep
%define buildversion %( echo %version | perl -pe "s/\./_/" )

%zsnes.prep -d %name-%version
cd %name-%version/zsnes_%buildversion
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir} -lsocket -lnsl"
export CXXFLAGS="%gcc_cxx_optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%zsnes.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%zsnes.install -d %name-%version
# --mandir option appears to do nothing
mkdir $RPM_BUILD_ROOT/%{_datadir}
mv $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT/%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Wed Dec 16 2011 - James Choi
- initial spec
