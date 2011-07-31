#
# spec file for package: llvm
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%include base.inc

%define src_name        llvm


Name:		SFEllvm
Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
SUNW_Copyright:	llvm.copyright
Version:	2.9
License:        BSD

URL:		http://llvm.org/
Source:		http://llvm.org/releases/%{version}/%{src_name}-%{version}.tgz
Source1:	http://llvm.org/releases/%{version}/clang-%{version}.tgz
Patch1:		llvm-01-limits.diff

Group:          Development
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}

%include default-depend.inc

BuildRequires:	SUNWlibtool
BuildRequires:	%pnm_buildrequires_perl_default
BuildRequires:	SUNWgroff
BuildRequires:	SUNWbison
BuildRequires:	SUNWflexlex
BuildRequires:	SUNWgmake
BuildRequires:	SFEgcc-45
Requires:	SFEgcc-45-runtime

%description
LLVM is a compiler infrastructure designed for compile-time, link-time, runtime,
and idle-time optimization of programs from arbitrary programming languages.
LLVM is written in C++ and has been developed since 2000 at the University of
Illinois and Apple. It currently supports compilation of C and C++ programs,
using front-ends derived from GCC 4.0.1. A new front-end for the C family of
languages is in development. The compiler infrastructure includes mirror sets of
programming tools as well as libraries with equivalent functionality.

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
cd tools && tar xzf %{SOURCE1} && mv clang-%{version} clang

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC="/usr/gcc/4.5/bin/gcc"
export CXX="/usr/gcc/4.5/bin/g++"

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/gcc/4.5/lib -R/usr/gcc/4.5/lib"

export PATH=$PATH:/usr/perl5/bin

./configure	--prefix=%{_prefix}		\
		--bindir=%{_bindir}		\
		--libdir=%{_libdir}        	\
		--includedir=%{_includedir}	\
		--mandir=%{_mandir}		\
		--datadir=%{_datadir}		\
		--disable-dependency-tracking	\
		--enable-optimized		\
		--disable-static		\
		--enable-shared
	
VERBOSE=1 make -j$CPUS

%install
rm -rf ${RPM_BUILD_ROOT}
export PATH=$PATH:/usr/perl5/bin

make install DESTDIR=${RPM_BUILD_ROOT}

mv ${RPM_BUILD_ROOT}/%{_prefix}/docs ${RPM_BUILD_ROOT}%{_datadir}/doc

%files
%defattr (-, root, bin)
%{_bindir}
%{_includedir}/clang
%{_includedir}/clang-c
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/llvm

%changelog
* Sat Jul 23 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Mon Apr 11 2011 - Milan Jurik
- bump to 2.9, add clang
*                 - Thomas Wagner
- migrated over from sourcejuicer
* Fri May  8 2009 <0xffea@googlemail.com>
- Initial spec
# trigger re-build
## Re-build 24/09/09
