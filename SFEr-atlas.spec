#
# spec file for package SFEr-atlas
#
# includes module(s): r-atlas
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%define srcname R

Name:                    SFEr-atlas
IPS_Package_Name:	 math/r-atlas
Summary:                 R - GNU S
Group:                   Utility
Version:                 2.15.1
URL:		         http://www.r-project.org
Source:		         http://cran.cnr.berkeley.edu/src/base/R-2/%{srcname}-%{version}.tar.gz
License: 		 GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEatlas
Requires: SFEatlas
BuildRequires: SUNWicud
Requires: SUNWicu
Requires: %pnm_requires_java_runtime_default

%description
R (“GNU S”), a language and environment for statistical computing and
graphics. R is similar to the award-winning S system, which was
developed at Bell Laboratories by John Chambers et al. It provides a
wide variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

# Note that this variant of R is built with ATLAS (Automatically Tuned
# Linear Algebra Software) which is probably what you want if you are
# building R for yourself but may not be if you are building shared
# binaries since you lose some of the benefit of the tuning. (At some
# point we should probably have multiarch for ATLAS.)

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LIBS="-lncurses"
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib -L/usr/lib/atlas"
export JAVA_HOME=/usr/java
export BLAS_LIBS="-L/usr/lib/atlas -lcblas -ltatlas"
export LAPACK_LIBS="-L/usr/lib/atlas -llapack -lcblas -ltatlas"
export CPPFLAGS="-I/usr/gnu/include"
./configure --prefix=%{_prefix}			\
            --with-lapack                       \
            --with-blas

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}/R
%{_libdir}/R/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Mon Oct 29 2012 - Logan Bruns <logan@gedanken.org>
- bump to 2.15.1, update depends, permissions and use shared atlas.
* Sat Apr 14 2012 - Logan Bruns <logan@gedanken.org>
- Rename to SFEr-atlas to keep atlas version separate. Maybe merge or
  replace old one if we change SFEatlas to be multiarch to better
  support the binary version of R plus atlas.
- Initial spec.
