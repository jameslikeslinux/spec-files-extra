#
# spec file for package SFEecl
#
# includes module(s): ecl
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define srcname ecl
%define major 12.2
%define minor 1

Name:                    SFEecl
IPS_Package_Name:	 runtime/lisp/ecl
Summary:                 ECL - Embeddable Common-Lisp
Group:                   Utility
Version:                 %{major}.%{minor}
URL:		         http://ecls.sourceforge.net
Source:		         %{sf_download}/project/ecls/ecls/%{major}/%{srcname}-%{major}.%{minor}.tgz
License: 		 LGPL or GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%define SFEgmp         %(/usr/bin/pkginfo -q SFEgmp 2>/dev/null  && echo 1 || echo 0)
%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

%description
ECL is an implementation of the Common Lisp language as defined by the
ANSI X3J13 specification. The most relevant features:

    A bytecodes compiler and interpreter.
    Compiles Lisp also with any C/C++ compiler.
    It can build standalone executables and libraries.
    ASDF, Sockets, Gray streams, MOP, and other useful components.
    Extremely portable.
    A reasonable license.

ECL supports the operating systems Linux, FreeBSD, NetBSD, OpenBSD,
Solaris and Windows, running on top of the Intel, Sparc, Alpha and
PowerPC processors. Porting to other architectures should be rather
easy.

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
export CFLAGS="%optflags -D_POSIX_PTHREAD_SEMANTICS"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --enable-threads

#Parallel build needs work
#make -j$CPUS
make

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
%{_libdir}/libecl.so
%dir %attr (0755, root, bin) %{_libdir}/ecl-%{version}
%{_libdir}/ecl-%{version}/*
%dir %attr(0755, root, sys) %{_includedir}/ecl
%{_includedir}/ecl/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Thu Jun 21 2012 - Logan Bruns <logan@gedanken.org>
- autodetect whether to use SFEgmp or system provided version.
* Tue Apr 17 2012 - Logan Bruns <logan@gedanken.org>
- Fixed some permissions.
* Sat Mar 24 2012 - Logan Bruns <logan@gedanken.org>
- Added --enable-threads flag.
* Mon Mar 12 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
