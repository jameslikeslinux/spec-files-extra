#
# spec file for package SFEmaxima
#
# includes module(s): maxima
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define srcname maxima

Name:                    SFEmaxima
IPS_Package_Name:	 math/maxima
Summary:                 Maxima - a Computer Algebra System
Group:                   Utility
Version:                 5.26.0
URL:		         http://maximas.sourceforge.net
Source:		         %{sf_download}/project/maxima/Maxima-source/%{version}-source/%{srcname}-%{version}.tar.gz
License: 		 GPL
Patch1:                  maxima-01-xerprn.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEecl

%description
Maxima is a system for the manipulation of symbolic and numerical
expressions, including differentiation, integration, Taylor series,
Laplace transforms, ordinary differential equations, systems of linear
equations, polynomials, and sets, lists, vectors, matrices, and
tensors. Maxima yields high precision numeric results by using exact
fractions, arbitrary precision integers, and variable precision
floating point numbers. Maxima can plot functions and data in two and
three dimensions.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
#export LDFLAGS="%_ldflags"
unset LDFLAGS
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --enable-ecl

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
%dir %attr (0755, root, bin) %{_libdir}/maxima
%{_libdir}/maxima/*
%dir %attr (0755, root, bin) %{_datadir}/maxima
%{_datadir}/maxima/*
%{_mandir}/man1/*
%{_datadir}/info/*

%changelog
* Tue Mar 13 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
