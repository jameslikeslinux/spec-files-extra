#
# spec file for package: llvm
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

### NOTE: The reason this spec is considered experimental is that
###       the sources have to be obtained by hand using Subversion.
###
###       svn co http://llvm.org/svn/llvm-project/llvm/trunk llvm
###       svn co http://llvm.org/svn/llvm-project/cfe/trunk clang
###
###       Then create xz-compressed tarballs of those directories
###       and place them into ~/packages/SOURCES.

### NOTE: Because of a bug in gcc, the following patch is required
###       to get llvm to build with gcc 4.6
###       http://gcc.gnu.org/bugzilla/show_bug.cgi?id=49347
#
# --- /usr/include/spawn.h.orig   2011-05-28 22:57:34.000000000 +0100
# +++ /usr/include/spawn.h        2011-07-20 00:06:04.429851081 +0100
# @@ -70,16 +70,16 @@
#         const char *_RESTRICT_KYWD path,
#         const posix_spawn_file_actions_t *file_actions,
#         const posix_spawnattr_t *_RESTRICT_KYWD attrp,
# -       char *const argv[_RESTRICT_KYWD],
# -       char *const envp[_RESTRICT_KYWD]);
# +       char *const *_RESTRICT_KYWD argv,
# +       char *const *_RESTRICT_KYWD envp);
#
#  extern int posix_spawnp(
#         pid_t *_RESTRICT_KYWD pid,
#         const char *_RESTRICT_KYWD file,
#         const posix_spawn_file_actions_t *file_actions,
#         const posix_spawnattr_t *_RESTRICT_KYWD attrp,
# -       char *const argv[_RESTRICT_KYWD],
# -       char *const envp[_RESTRICT_KYWD]);
# +       char *const *_RESTRICT_KYWD argv,
# +       char *const *_RESTRICT_KYWD envp);
 
#  extern int posix_spawn_file_actions_init(
#         posix_spawn_file_actions_t *file_actions);


%include Solaris.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%include base.inc

%define src_name        llvm
%define revision	135557


Name:		SFEllvm
Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
SUNW_Copyright:	llvm.copyright
Version:	2.9.99.%revision
License:        BSD
URL:		http://llvm.org/
#Source:	http://llvm.org/releases/%{version}/%{src_name}-%{version}.tgz
#Source1:	http://llvm.org/releases/%{version}/clang-%{version}.tgz
Source:		%src_name-%revision.txz
Source1:	clang-%revision.txz
Patch1:		llvm-01-limits.diff

Group:          Development/C
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}

%include default-depend.inc

BuildRequires:	SUNWlibtool
BuildRequires:	%pnm_buildrequires_perl_default
BuildRequires:	SUNWgroff
BuildRequires:	SUNWbison
BuildRequires:	SUNWflexlex
BuildRequires:	SUNWgmake
BuildRequires:	SFEgcc
Requires:	SFEgccruntime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%description
LLVM is a compiler infrastructure designed for compile-time, link-time, runtime,
and idle-time optimization of programs from arbitrary programming languages.
LLVM is written in C++ and has been developed since 2000 at the University of
Illinois and Apple. It currently supports compilation of C and C++ programs,
using front-ends derived from GCC 4.0.1. A new front-end for the C family of
languages is in development. The compiler infrastructure includes mirror sets of
programming tools as well as libraries with equivalent functionality.

%prep
%setup -q -n %{src_name}
%patch1 -p1
cd tools && gtar -xJf %{SOURCE1}

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
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
	
#VERBOSE=1 make -j$CPUS
make -j$CPUS

%install
rm -rf ${RPM_BUILD_ROOT}
export PATH=$PATH:/usr/perl5/bin

make install DESTDIR=${RPM_BUILD_ROOT}

mv ${RPM_BUILD_ROOT}/%{_prefix}/docs ${RPM_BUILD_ROOT}%{_datadir}/doc

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_bindir}
%{_includedir}/clang
%{_includedir}/clang-c
%{_includedir}/llvm
%{_includedir}/llvm-c
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/llvm

%changelog
* Sat Jul 23 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sun Jul 17 2011 - Alex Viskovatoff
- fork new spec off SFEllvm.spec, using development version from SVN
- do not hardcode gcc version: use /usr/gnu/bin/gcc
* Mon Apr 11 2011 - Milan Jurik
- bump to 2.9, add clang
*                 - Thomas Wagner
- migrated over from sourcejuicer
* Fri May  8 2009 <0xffea@googlemail.com>
- Initial spec
# trigger re-build
## Re-build 24/09/09
