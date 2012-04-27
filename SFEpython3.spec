#
# spec file for package SFEpython3
#
#

%define src_name Python
%define version 3.2.3
%define unmangled_version 3.2.3

%include Solaris.inc

Name: SFEpython3
IPS_Package_Name:	runtime/python-32
Summary: The Python interpreter, libraries and utilities
Group: Development/Python
Version: %{version}
License: PSF license
Source: http://www.python.org/ftp/python/%{unmangled_version}/%{src_name}-%{unmangled_version}.tar.bz2
URL: http://www.python.org/

%include default-depend.inc

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
SUNW_Basedir:	%{_basedir}
SUNW_Copyright:	Python3.copyright

# OpenSolaris IPS Manifest Fields
Meta(info.maintainer): A Hettinger <ahettinger@prominic.net>
Meta(info.upstream):  Guido van Rossum and the Python community <python-dev@python.org>
Meta(info.repository_url): http://svn.python.org/projects/python/branches/release32-maint
Meta(info.classification): org.opensolaris.category.2008:Development/Python


%description
Python is an interpreted, interactive, object-oriented programming
language. It is often compared to Tcl, Perl, Scheme or Java.

Python combines remarkable power with very clear syntax. It has
modules, classes, exceptions, very high level dynamic data types, and
dynamic typing. There are interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac, MFC). New built-in modules are easily written in C or C++. Python
is also usable as an extension language for applications that need a
programmable interface.

The Python implementation is portable: it runs on many brands of UNIX,
on Windows, DOS, OS/2, Mac, Amiga... If your favorite system isn't
listed here, it may still be supported, if there's a C compiler for
it. Ask around on comp.lang.python -- or just try compiling Python
yourself.

%prep
%setup -n %{src_name}-%{unmangled_version}

%build
CPUS=$(psrinfo | awk '$2=="on-line"{cpus++}END{if(cpus==0){print 1}else{print cpus }}')

env CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} \
					--mandir=%{_mandir}
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Collision with other pythons
rm -f $RPM_BUILD_ROOT/%{_bindir}/2to3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/idle3
%{_bindir}/idle3.2
#%{_bindir}/2to3
%{_bindir}/2to3-3.2
%{_bindir}/python3
%{_bindir}/python3.2
%{_bindir}/python3.2m
%{_bindir}/python3-config
%{_bindir}/python3.2-config
%{_bindir}/python3.2m-config
%{_bindir}/pydoc3
%{_bindir}/pydoc3.2
%dir %attr (-, root, bin) %{_libdir}
%{_libdir}/python3.2/*
%dir %attr (-, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/python3.pc
%{_libdir}/pkgconfig/python-3.2m.pc
%{_libdir}/pkgconfig/python-3.2.pc
%{_libdir}/libpython3.2m.a
%dir %attr(-,root,sys) %{_datadir}
%dir %attr(-, root, bin) %{_mandir}
%dir %attr(-, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr(-, root, bin) %{_includedir}
%{_includedir}/python3.2m/*

%changelog
* Fri Apr 27 2012 - Milan Jurik
- bump to 3.2.3
- fix packaging
* Wed Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 3.2.2
* Wed June 29, 2011 - A Hettinger <ahettinger@prominic.net>
- Initial .spec
* Sun Jul 3, 2011 - A Hettinger <ahettinger@prominic.net>
- the ternary operator is not supported in anchient versions of awk
