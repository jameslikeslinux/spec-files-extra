#
# spec file for package SFEsage
#
# includes module(s): sage
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


%include Solaris.inc

%define cc_is_gcc 1
# Solaris.inc's define includes -DPIC which breaks some code
%define gcc_picflags -fPIC
%include base.inc

%define srcname sage

Name:                    SFEsage
IPS_Package_Name:	 sfe/math/sage
Summary:                 SAGE - a free open-source mathematics software system
Group:                   Utility
Version:                 5.0
URL:		         http://sagemath.info
Source:		         http://www.sagemath.org/src-old/sage-%{version}.tar
License: 		 GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Sage is free, open-source math software that supports research and
teaching in algebra, geometry, number theory, cryptography, numerical
computation, and related areas. Both the Sage development model and
the technology in Sage itself are distinguished by an extremely strong
emphasis on openness, community, cooperation, and collaboration: we
are building the car, not reinventing the wheel. The overall goal of
Sage is to create a viable, free, open-source alternative to Maple,
Mathematica, Magma, and MATLAB.

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
export LD=/usr/ccs/bin/ld

#make MAKE="make -j$CPUS"
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share
mv $RPM_BUILD_ROOT/sage $RPM_BUILD_ROOT/usr/share
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -s /usr/share/sage/sage $RPM_BUILD_ROOT/usr/bin/sage
rm -rf $RPM_BUILD_ROOT/bin
rm $RPM_BUILD_ROOT/usr/share/sage/*.log 
rm $RPM_BUILD_ROOT/usr/share/sage/spkg/logs/*.log

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%defattr (-, root, bin)
%dir %attr(0755, root, other) %{_datadir}/sage
%{_datadir}/sage/*

%changelog
* Tue Jun 19 2012 - Logan Bruns <logan@gedanken.org>
- Fixed download URL (avoid mirror which changed.)
* Thu Jun 7 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
