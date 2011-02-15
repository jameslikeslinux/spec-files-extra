#
# spec file for package: llvm
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc
%define src_name        llvm


Name:		SFEllvm
Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
Version:	2.5
License:        University of Illinois/NCSA Open Source License

URL:		http://llvm.org/
Source:		http://llvm.org/releases/%{version}/%{src_name}-%{version}.tar.gz

Group:          Development
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}
SUNW_Copyright: %{name}.copyright

Patch1:		llvm-01-pod2html.diff

%include default-depend.inc

BuildRequires:	SUNWlibtool
BuildRequires:	SUNWperl584usr
BuildRequires:	SUNWgroff
BuildRequires:	SUNWgcc
BuildRequires:	SUNWbison
BuildRequires:	SUNWflexlex
BuildRequires:	SUNWgmake


# OpenSolaris IPS Manifest Fields
Meta(info.upstream):		Chris Lattner <sabre@nondot.org>
Meta(info.maintainer):		David Höppner <0xffea@googlemail.com>
Meta(info.repository_url):	http://llvm.org/svn/llvm-project/llvm/trunk
Meta(info.classification):	org.opensolaris.category.2008: Development/C

%description
LLVM is a compiler infrastructure designed for compile-time, link-time, runtime,
and idle-time optimization of programs from arbitrary programming languages.
LLVM is written in C++ and has been developed since 2000 at the University of
Illinois and Apple. It currently supports compilation of C and C++ programs,
using front-ends derived from GCC 4.0.1. A new front-end for the C family of
languages is in development. The compiler infrastructure
includes mirror sets of programming tools as well as libraries with equivalent
functionality.

%prep
%setup -q -n %{src_name}-%{version}

%patch1	-p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC="/usr/sfw/bin/gcc"
export CXX="/usr/sfw/bin/g++"

export POD2HTML="/usr/perl5/5.8.4/bin/pod2html"
export POD2MAN="/usr/perl5/5.8.4/bin/pod2man"

#export CFLAGS="%{gcc_optflags}"
#export LDFLAGS="%{_ldflags}"

./configure	--prefix=%{_prefix}		\
		--bindir=%{_bindir}		\
		--libdir=%{_libdir}        	\
		--includedir=%{_includedir}	\
		--mandir=%{_mandir}		\
		--datadir=%{_datadir}		\
		--disable-dependency-tracking	\
		--enable-optimized		\
		--enable-assertions
	
gmake -j$CPUS

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

mv ${RPM_BUILD_ROOT}/%{_prefix}/docs ${RPM_BUILD_ROOT}%{_datadir}/doc

%files
%defattr (-, root, root)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/llvm-config
%{_bindir}/gccas
%{_bindir}/gccld
%{_bindir}/opt
%{_bindir}/llvm-as
%{_bindir}/llvm-dis
%{_bindir}/llc
%{_bindir}/llvm-ranlib
%{_bindir}/llvm-ar
%{_bindir}/llvm-nm
%{_bindir}/llvm-ld
%{_bindir}/llvm-prof
%{_bindir}/llvm-link
%{_bindir}/lli
%{_bindir}/llvm-extract
%{_bindir}/llvm-db
%{_bindir}/bugpoint
%{_bindir}/llvm-bcanalyzer
%{_bindir}/llvm-stub
%{_bindir}/llvmc

%dir %attr (0755, root, sys) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%dir %attr (0755, root, sys) %{_mandir}
%dir %attr (0755, root, sys) %{_mandir}/man1
%{_mandir}/man1/bugpoint.1
%{_mandir}/man1/llc.1
%{_mandir}/man1/lli.1
%{_mandir}/man1/llvm-ar.1
%{_mandir}/man1/llvm-as.1
%{_mandir}/man1/llvm-bcanalyzer.1
%{_mandir}/man1/llvm-config.1
%{_mandir}/man1/llvmc.1
%{_mandir}/man1/llvm-db.1
%{_mandir}/man1/llvm-dis.1
%{_mandir}/man1/llvm-extract.1
%{_mandir}/man1/llvmgcc.1
%{_mandir}/man1/llvmgxx.1
%{_mandir}/man1/llvm-ld.1
%{_mandir}/man1/llvm-link.1
%{_mandir}/man1/llvm-nm.1
%{_mandir}/man1/llvm-prof.1
%{_mandir}/man1/llvm-ranlib.1
%{_mandir}/man1/opt.1
%{_mandir}/man1/tblgen.1


%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/doc/*

%changelog
*                 - Thomas Wagner
- migrated over from sourcejuicer
* Fri May  8 2009 <0xffea@googlemail.com>
- Initial spec
# trigger re-build
## Re-build 24/09/09
