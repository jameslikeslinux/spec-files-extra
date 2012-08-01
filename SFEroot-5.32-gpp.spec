#
# spec file for package SFEroot-gpp
#
# includes module(s): root
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

# Do Not update this file beyond 5.32.X.
# Just copypasta into a new spec for the next revision.
# Future victims of obsoleted code thank you!
%define rootversion 5.32.00

# Decide which ROOT extensions to build
# TODO: more extensions
%define with_roofit 1
%define with_python 1
%define with_pythia8 0
%define with_mathmore 0

%define majorversion %(echo %{rootversion} | cut -d "." -f1-2)
%define majorversiony %(echo %{majorversion} | tr '.' '-')

# TODO: differentiate libraries by SunCC, ICC, GCC3, etc
#%define _prefix /opt/ROOT/%{root.version}.gcc4 or something
%define _prefix /opt/ROOT/%{majorversion}
%define _rootsysconfdir %{_prefix}/etc

%use root = root.spec

Name:                    SFEroot%{majorversiony}-gpp
IPS_Package_Name:	 library/desktop/g++/root
Summary:                 ROOT - Toolkit for Physics Analysis
Group:                   Applications/Math
License:                 LGPL
Version:                 %{rootversion}

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Requires: SFEgcc
#Requires: SFEgccruntime
#Requires: SUNWlibC
#BuildRequires: SFEgcc
#BuildRequires: SFEgccruntime
#BuildRequires: x11/library/libxft
#BuildRequires: SFElibglew
#BuildRequires: SFEpcre-gpp
#%if %with_python
#Requires: SFEpython
#BuildRequires: pkg:/runtime/python-26
#BuildRequires: SUNWpython-devel
#%endif
%if %with_pythia8
Requires: SFEpythia8
BuildRequires: SFEpythia8-devel
%endif
%if %with_mathmore
Requires: SFEgsl
BuildRequires: SFEgsl-devel
%endif
#Requires: SFEglibmm-gpp

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	/
%include default-depend.inc
Requires: %name

# RooFit extension packages
%if %with_roofit
%package roofit
Summary:	RooFit - ROOT extension for modeling expected distribtions
SUNW_BaseDir:	/
%include default-depend.inc
Requires: %name

%package roofit-devel
Summary:	RooFit - ROOT extension - development files
SUNW_BaseDir:	/
%include default-depend.inc
Requires: %name
Requires: %name-roofit
%endif  #if %with_roofit

# Python extension packages
%if %with_python
%package python
Summary:	%{summary} - Python plug-in for ROOT
SUNW_BaseDir:	/
%include default-depend.inc
Requires: %name

%package python-devel
Summary:        ROOT Python plug-in - development files
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Requires: %name-python
%endif  #if %with_python


%prep
rm -rf %name-%version
mkdir %name-%version
%root.prep -d %name-%version

%build
#%if %with_suncc
#export CC="cc -m32"
#export CXX="CC -m32"
#export CXXFLAGS="-library=stlport4"
#export SHLIB_CXXFLAGS="-library=stlport4"
#export SHLIB_CXXLD="CC -m32 "
#export SHLIB_CXXFLAGS="-library=stlport4"
#export SHLIB_CXXLDFLAGS="-G -library=stlport4"
#export F77="f95 -m32"
#export FC="f95 -m32"
#endif
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib"
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
export MAKE=gmake
%root.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
export MAKE=gmake
%root.install -d %name-%version

# Default install installs a troubling amount of garbage
# Eliminate empty/useless directories
cd $RPM_BUILD_ROOT%{_datadir}
gfind . -depth -type d -empty -exec rmdir {} \;
rm -r $RPM_BUILD_ROOT%{_rootsysconfdir}/vmc
rm -r $RPM_BUILD_ROOT%{_bindir}/*.exe
# Move mandir away temporarily before list madness
mv $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT/tempman

# Prepare lists of files for packaging
cd %{_builddir}/%name-%version
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*" > ROOT-all.files
find $RPM_BUILD_ROOT%{_includedir} -type f -name "*" > ROOT-all.dev.files
find $RPM_BUILD_ROOT%{_datadir}/doc/root/* -type f >> ROOT-all.dev.files
sort ROOT-all.files > ROOT-all-sort.files
sort ROOT-all.dev.files > ROOT-all-sort.dev.files

# RooFit files
%if %with_roofit
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "libRoo*" > roofit.files
find $RPM_BUILD_ROOT/%{_includedir}/root -type f -name "Roo*" > roofit.dev.files
#find $RPM_BUILD_ROOT/%{_includedir}/doc/ -type f -name "libroot-roofit%{majorversion}*" >> roofit.dev.files
#find $RPM_BUILD_ROOT/%{_includedir}/doc/ -type f -name "libroot-roofit-dev%{majorversion}*" >> roofit.dev.files
sort roofit.files > roofit-sort.files
sort roofit.dev.files > roofit-sort.dev.files
comm -23 ROOT-all-sort.files roofit-sort.files > TEMP \
     && mv TEMP ROOT-all-sort.files
comm -23 ROOT-all-sort.dev.files roofit-sort.dev.files > TEMP \
     && mv TEMP ROOT-all-sort.dev.files
%endif  #if %with_roofit

# PyRoot files
%if %with_python
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "libPyROOT*" > pyroot.files
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.py" > pyroot.dev.files
find $RPM_BUILD_ROOT/%{_includedir}/root -type f -name "TPy*" >> pyroot.dev.files
#find $RPM_BUILD_ROOT/%{_includedir}/doc/ -type f -name "libroot-python%{majorversion}*" >> pyroot.dev.files
#find $RPM_BUILD_ROOT/%{_includedir}/doc/ -type f -name "libroot-python-dev%{majorversion}*" >> pyroot.dev.files
sort pyroot.files > pyroot-sort.files
sort pyroot.dev.files > pyroot-sort.dev.files
comm -23 ROOT-all-sort.files pyroot-sort.files > TEMP \
     && mv TEMP ROOT-all-sort.files
comm -23 ROOT-all-sort.dev.files pyroot-sort.dev.files > TEMP \
     && mv TEMP ROOT-all-sort.dev.files
%endif  #if %with_python

# Pythia files
%if %with_pythia8
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*Pythia8.so" > pythia8.files
find $RPM_BUILD_ROOT/%{_includedir} -type f -name "*Pythia8.h" > pythia8.dev.files
#find $RPM_BUILD_ROOT/%{_includedir}/root -type f -name "TPy*" >> pythia8.dev.files
#find $RPM_BUILD_ROOT/%{_includedir}/doc/ -type f -name "libroot-pythia8%{majorversion}*" >> pythia8.dev.files
#find $RPM_BUILD_ROOT/%{_includedir}/doc/ -type f -name "libroot-pythia8-dev%{majorversion}*" >> pythia8.dev.files
sort pythia8.files > pythia8-sort.files
sort pythia8.dev.files > pythia8-sort.dev.files
comm -23 ROOT-all-sort.files pythia8-sort.files > TEMP \
     && mv TEMP ROOT-all-sort.files
comm -23 ROOT-all-sort.dev.files pythia8-sort.dev.files > TEMP \
     && mv TEMP ROOT-all-sort.dev.files
%endif  #if %with_pythia8




# Clean up syntax for %files section
cat ROOT-all-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > ROOT.files
cat ROOT-all-sort.dev.files | sed 's:'"$RPM_BUILD_ROOT"'::' > ROOT.dev.files
%if %with_roofit
cat roofit-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > roofit.files
cat roofit-sort.dev.files | sed 's:'"$RPM_BUILD_ROOT"'::' > roofit.dev.files
%endif  #if %with_roofit
%if %with_python
cat pyroot-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > pyroot.files
cat pyroot-sort.dev.files | sed 's:'"$RPM_BUILD_ROOT"'::' > pyroot.dev.files
%endif  #if %with_python
%if %with_pythia8
cat pythia8-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > pythia8.files
cat pythia8-sort.dev.files | sed 's:'"$RPM_BUILD_ROOT"'::' > pythia8.dev.files
%endif  #if %with_pythia8

# Finally, move mandir back
mv $RPM_BUILD_ROOT/tempman $RPM_BUILD_ROOT%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


# TODO: these files are not being classified 100% correctly
#  includedir needs better granularity between dev/normal pkgs
#  mandirs ought to be separated amongst consistuent pkgs
%files -f ROOT.files
%defattr (-, root, bin)
%{_bindir}/g2root
%{_bindir}/genreflex
%{_bindir}/genreflex-rootcint
%{_bindir}/h2root
%{_bindir}/hadd
%{_bindir}/hist2workspace
%{_bindir}/pq2
%{_bindir}/prepareHistFactory
%{_bindir}/proofd
%{_bindir}/proofserv
%{_bindir}/root
%{_bindir}/rootd
%{_bindir}/roots
%{_bindir}/ssh2rpd
%{_bindir}/setxrd.sh
%{_bindir}/setxrd.csh
%{_bindir}/thisroot.sh
%{_bindir}/thisroot.csh
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/icons
%{_datadir}/macros
##%{_datadir}/lintian/overrides/libroot%{majorversion}
%dir %attr (0755, root, sys) %{_rootsysconfdir}
%{_rootsysconfdir}/*

%files devel -f ROOT.dev.files
%defattr (-, root, bin)
%{_bindir}/genmap
%{_bindir}/memprobe
%{_bindir}/rlibmap
%{_bindir}/rmkdepend
%{_bindir}/root-config
%{_bindir}/rootcint
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/fonts
%{_datadir}/emacs/site-lisp/root-help.el
%{_datadir}/aclocal/root.m4
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

# RooFit extension packages
%if %with_roofit
%files roofit -f roofit.files
%defattr (-, root, bin)
##%{_datadir}/lintian/overrides/libroot-roofit%{majorversion}

%files roofit-devel -f roofit.dev.files
%defattr (-, root, bin)
%endif  #if %with_roofit

# Python extension packages
%if %with_python
%files python -f pyroot.files
%defattr (-, root, bin)

%files python-devel -f pyroot.dev.files
%defattr (-, root, bin)
%endif  #if %with_python

# Pythia8 extension packages
%if %with_pythia8
%files python -f pythia8.files
%defattr (-, root, bin)

%files python-devel -f pythia8.dev.files
%defattr (-, root, bin)
%endif  #if %with_pythia8


%changelog
* Thu Oct 4 2009 - James Choi <jchoi42@pha.jhu.edu>
- Initial spec
