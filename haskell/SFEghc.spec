#
# spec file for package SFEghc 
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define is_amd64        %( test "`isalist | cut -d' ' -f1`" = "amd64" && echo 1 || echo 0 )

%define is_s10		%( test "`uname -r`" = "5.10" && echo 1 || echo 0 )
%if %{is_s10}
%define osbuild "10"
%else
%define osbuild %(uname -v | sed -e 's/[A-z_]//g')
%endif

%define osgooglecode http://opensolaris-lang.googlecode.com/files
%define bootstrap 6.12.3

Name:		SFEghc 
Summary:	The Glorious Glasgow Haskell Compilation System
Version:	6.12.3
Release:	1
License:	GHC License
Group:		Development/Languages/Haskell
Vendor:		GHC team
URL:		http://www.haskell.org/ghc
Source:		%url/dist/%version/ghc-%version-src.tar.bz2
Source1:	%osgooglecode/ghc-%bootstrap-i386.tar.xz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build

%description
Haskell is the standard lazy purely functional programming language.
The current language version is Haskell 98, agreed in December 1998,
with a revised version published in January 2003. The Haskell 2000
report was published in July 2010.

GHC is a state-of-the-art programming suite for Haskell. Included is
an optimising compiler generating good code for a variety of
platforms, together with an interactive system for convenient, quick
development. The distribution includes space and time profiling
facilities, a large collection of libraries, and support for various
language extensions, including concurrency, exceptions, and foreign
language interfaces (C, C++, whatever). Since version 7.0.2, GHC
supports DTrace on Solaris.

A wide variety of Haskell related resources (tutorials, libraries,
specifications, documentation, compilers, interpreters, references,
contact information, links to research groups) are available from the
Haskell home page at http://haskell.org/.


%define SFEgmp          %(/usr/bin/pkginfo -q SUNWgnu-mp && echo 0 || echo 1)
%define SFEmpfr         %(/usr/bin/pkginfo -q SUNWgnu-mpfr && echo 0 || echo 1)
%define SFEreadline     %(/usr/bin/pkginfo -q SUNWgnu-readline && echo 0 || echo 1)
%define SFEncurses      %(/usr/bin/pkginfo -q SUNWncurses && echo 0 || echo 1)

%include default-depend.inc

BuildRequires: 	SUNWgcc
BuildRequires:	SUNWgsed
BuildRequires:	SFExz
Requires: 	SUNWgccruntime

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

%if %SFEmpfr
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
%else
BuildRequires: SUNWgnu-mpfr
Requires: SUNWgnu-mpfr
%endif

BuildRequires: SUNWesu

%if %SFEreadline
Requires: SFEreadline
%else
Requires: SUNWgnu-readline
%endif

%if %SFEncurses
BuildRequires: SFEncurses
%else
BuildRequires: SUNWncurses
%endif

%package prof
Summary:                 %{summary} - profiling libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}


%prep
%setup -q -n ghc-%version
cd /var/tmp
rm -rf ghc-%bootstrap-bin
xz -dc %SOURCE1 | tar -xf -


%build

export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%_libdir/pkgconfig"
export PATH=$PATH:/var/tmp/ghc-%bootstrap-bin/bin

%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
export LDFLAGS='-L/usr/gnu/lib -R/usr/gnu/lib'
%else
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
%endif

CPUS=$(psrinfo | awk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

chmod +x configure
# Note GHC conf does not support differing host/target (i.e., cross-compiling)
./configure --prefix=%_prefix \
    --with-ghc=/var/tmp/ghc-%bootstrap-bin/bin/ghc \
    --with-gcc=/usr/bin/gcc --with-ld=/usr/bin/ld \
%if %{is_s10}
    --with-gmp-includes=/usr/gnu/include    \
    --with-gmp-libraries=/usr/gnu/lib
%else
     --with-gmp-includes=/usr/include/gmp    \
     --with-gmp-libraries=/usr/include/gmp   
%endif

# Parallelism breaks with 16 cpus, so don't use more than 4
gmake -j$(test $CPUS -ge 4 && echo 4 || echo $CPUS)

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT VERBOSE=1

# Need to create this symlink so that the hyperlink from file://localhost/usr/share/doc/ghc/html/index.html
# to the GHC API file://localhost/usr/share/doc/ghc/html/libraries/ghc/index.html will find it at:
# file://localhost/usr/share/doc/ghc/html/libraries/ghc-6.12.1/index.html
pushd $RPM_BUILD_ROOT%{_docdir}/ghc/html/libraries
ln -s ghc-%{version} ghc
popd

# Prepare lists of files for packaging
cd %{_builddir}/ghc-%{version}
touch ghc6.files ghc6-prof.files ghc6-all.files
find $RPM_BUILD_ROOT -type f -name "*.p_hi" > ghc6-prof.files
find $RPM_BUILD_ROOT -type f -name "*_p.a" >> ghc6-prof.files

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*" > ghc6-all.files

sort ghc6-prof.files > ghc6-prof-sort.files
sort ghc6-all.files > ghc6-all-sort.files
comm -23 ghc6-all-sort.files ghc6-prof-sort.files > ghc6.files

# Clean up syntax for %files section
cat ghc6.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP ghc6.files
cat ghc6-prof-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP ghc6-prof.files

# Remove extra documentation
#rm -r $RPM_BUILD_ROOT/usr/share*
# Manpages aren't building for some reason... steal from prebuilt!
### cp -r %{_builddir}/%{name}-%{version}/postbuilt/share/man* $RPM_BUILD_ROOT/usr/share/

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf /var/tmp/ghc-%bootstrap-bin


%files -f ghc6.files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/*

%files prof -f ghc6-prof.files
%defattr (-, root, bin)

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*


%changelog
* Wed Apr 20 2011 - Alex Viskovatoff
- Go back to 6.12.3, to use official source tarball
* Sun Mar 27 2011 - Alex Viskovatoff
- Update to 7.1 taken from darcs HEAD; 7.0.y does not build on Solaris
- Use gcc 3.4.3: ghc 7.x does not build on later releases of gcc
- Use custom bootstrap tarball
* Mon July 19 2010 - markwright@internode.on.net
- Bump to 6.12.3
* May 3 2010 - Gilles Dauphin
- Get ready for next release
- find in _libdir
* Thu Apr 8 2010 - markwright@internode.on.net
- Bump to 6.12.1
* Sun Sep 6 2009 - jchoi42@pha.jhu.edu
- Initial spec
