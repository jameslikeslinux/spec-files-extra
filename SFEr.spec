#
# spec file for package SFEr
#
# includes module(s): r
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%define srcname R

Name:                    SFEr
IPS_Package_Name:	 math/r
Summary:                 R - GNU S
Group:                   Utility
Version:                 2.15.0
URL:		         http://www.r-project.org
Source:		         http://cran.cnr.berkeley.edu/src/base/R-2/%{srcname}-%{version}.tar.gz
License: 		 GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: math/atlas
Requires: %pnm_requires_java_runtime_default

%description
R (“GNU S”), a language and environment for statistical computing and
graphics. R is similar to the award-winning S system, which was
developed at Bell Laboratories by John Chambers et al. It provides a
wide variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

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
export BLAS_LIBS="-L/usr/lib/atlas -lcblas -latlas"
export LAPACK_LIBS="-L/usr/lib/atlas -llapack -lcblas -latlas"
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
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}/R
%{_libdir}/R/*
%{_mandir}/man1/*

%changelog
* Sat Apr 14 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
