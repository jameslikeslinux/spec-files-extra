#
# spec file for package SFEpari
#
# includes module(s): pari
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname pari

Name:                    SFEpari
IPS_Package_Name:	 math/pari
Summary:                 PARI/GP - a Computer Algebra System
Group:                   Utility
Version:                 2.5.1
URL:		         http://pari.math.u-bordeaux.fr
Source:		         http://pari.math.u-bordeaux.fr/pub/pari/unix/pari-%{version}.tar.gz
License: 		 GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: system/library/gmp

%description
PARI/GP is a widely used computer algebra system designed for fast
computations in number theory (factorizations, algebraic number
theory, elliptic curves...), but also contains a large number of other
useful functions to compute with mathematical entities such as
matrices, polynomials, power series, algebraic numbers etc., and a lot
of transcendental functions. PARI is also available as a C library to
allow for faster computations.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="-R/usr/gnu/lib"
./Configure --prefix=%{_prefix}			\
            --share-prefix=%{_datadir}          \
	    --bindir=%{_bindir}			\
	    --includedir=%{_includedir}  	\
	    --mandir=%{_mandir}/man1		\
            --libdir=%{_libdir}                 \
            --with-gmp                          \
            --with-gmp-include=/usr/include/gmp \
            --with-readline                     \
            --with-ncurses-lib=/usr/gnu/lib

make -j$CPUS all

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libpari*
%dir %attr (0755, root, bin) %{_libdir}/pari
%{_libdir}/pari/*
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/pari
%{_includedir}/pari/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pari
%{_datadir}/pari/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Tue May 1 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
