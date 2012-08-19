#
# spec file for package SFEgcc
#
# includes module(s): GNU gcc
#

# owner:  Thomas Wagner
#

##TODO## test sparc version of gcc-05-LINK_LIBGCC_SPEC-sparcv9.diff

#provide symbolic links in places define below:
#start the paths with a leading "/"
#example:   %define gccsymlinks /usr/gcc /usr/gnu

%define gccsymlinks /usr/gcc /usr/gnu
#IMPORTANT! READ ON BELOW and set switches and paths accordingly

#hack for the %files section. use define for each directory from above
#to control the non scriptable %files section
#1 = enabled    0 = disabled
#and special<n>path point to one of the paths noted in %{gccsymlinks}
%define symlinktarget1enabled      1
%define symlinktarget1path /usr/gcc

%define symlinktarget2enabled      1
%define symlinktarget2path /usr/gnu

#spare
%define symlinktarget3enabled      0
%define symlinktarget3path /usr

# check for /usr/gnu/bin/cc and bail out
# CR 7031722 (Solaris)
# Bug-ID <TBD> (OI)
%define compat_link_usr_gnu_bin_cc %( test -r /usr/gnu/bin/cc && echo 1 || echo 0 )

# to more widely test if this change causes regressions, by default off:
# want this? compile with: --with-handle_pragma_pack_push_pop
%define with_handle_pragma_pack_push_pop %{?_with_handle_pragma_pack_push_pop:1}%{?!_with_handle_pragma_pack_push_pop:0}

%include Solaris.inc
%include base.inc

%define osbuild %(uname -v | sed -e 's/[A-z_]//g')

##TODO## should include/arch64.inc consider setting _arch64 that way?
#        gcc builds 64-bit libs/binaries even on 32-bit CPUs/Kernels (e.g. ATOM CPU)
%ifarch amd64 i386
%define _arch64 amd64
%else
%define _arch64 sparcv9
%endif


#default to SUNWbinutils
##TODO## if necessary add osbuild numbers to decide SUNW/SFE version
%define SUNWbinutils    %(/usr/bin/pkginfo -q SUNWbinutils 2>/dev/null && echo 1 || echo 0)
%define SFEbinutils     %(/usr/bin/pkginfo -q SFEbinutils  2>/dev/null && echo 1 || echo 0)
#see below, older builds then 126 have too old gmp / mpfr to gcc version around 4.4.4
#%define SFEgmp          %(/usr/bin/pkginfo -q SFEgmp  2>/dev/null  && echo 1 || echo 0)
##TODO## to be replaced by packagenamemacros, selecting SFEgmp on specific osbuilds where
#it is too old for fresh gcc builds
%define SFEgmp          1
#%define SFEmpfr         %(/usr/bin/pkginfo -q SFEmpfr 2>/dev/null  && echo 1 || echo 0)
##TODO## to be replaced by packagenamemacros, selecting SFEmpfr on specific osbuilds where
#it is too old for fresh gcc builds
%define SFEmpfr         1

# force using SFEbinutils
#if SFEbinutils is not present, force it by the commandline switch --with_SFEbinutils
%define with_SFEbinutils %{?_with_SFEbinutils:1}%{?!_with_SFEbinutils:0}
%if %with_SFEbinutils
%define SFEbinutils 1
%define SUNWbinutils 0
%endif

# force using gmp | mpfr
#if SFEgmp is not present, force them as required by the commandline switch --with_SFEgmp
%define with_SFEgmp %{?_with_SFEgmp:1}%{?!_with_SFEgmp:0}
#if build is lower then 126 then force it (update to gmp see CR 6863696)
%if %(expr %{osbuild} '<' 126)
%define with_SFEgmp 1
%endif

%if %with_SFEgmp
%define SFEgmp 1
%endif

#if SFEgmp is not present, force them as required by the commandline switch --with_SFEmpfr
%define with_SFEmpfr %{?_with_SFEmpfr:1}%{?!_with_SFEmpfr:0}
#if build is lower then 126 then force it (update to gmp see CR 6863684)
%if %(expr %{osbuild} '<' 126)
%define with_SFEmpfr 1
%endif

%if %with_SFEmpfr
%define SFEmpfr 1
%endif

#if SFElibmpc is not present, force them as required by the commandline switch --with-SFElibmpc
#future OS versins might include a libmpc, leave code commented until then
%define with_SFElibmpc %{?_with_SFElibmpc:1}%{?!_with_SFElibmpc:0}
#parked #if build is lower then 126 then force it (update to gmp see CR 6863684)
#parked %if %(expr %{osbuild} '<' 126)
#for *now* require SFElibmpc in any case
%define with_SFElibmpc 1
#parked %endif

%if %with_SFElibmpc
%define SFElibmpc 1
%endif

#if you want a specific version of gcc be built, then change the default setting
#below *or* specify the number on the command line (gcc_version), example see below

# To set a specific gcc version to be build, do this from *outside*
# pkgtool build SFEgcc --define 'gcc_version 4.6.1'

%if %{!?gcc_version:1}
#make version bump *here* - this is the default version being built
%define version 4.6.3
%else
#gcc version is already defined from *outside*, from the pkgtool command line
%define version %{gcc_version}
%endif
#special handling of version / gcc_version

#transform full version to short version: 4.6.2 -> 4.6  or  4.7.1 -> 4.7
#%define major_minor %( echo %{version} | sed -e 's/\([0-9]*\)\.\([0-9]*\)\..*/\1.\2/' )
#below is a workaround for pkgbuild 1.3.104 failing to parse the escaped \( and \)
%define major_minor %( echo %{version} |  sed -e 's/\.[0-9]*$//' )

#for package or path names we need the version number _without_ the dots:
#transform dottet version number to non-dotted:  4.6 -> 46
%define majorminornumber %( echo %{major_minor} | sed -e 's/\.//g' )
%define _prefix /usr/gcc/%major_minor
%define _infodir %{_prefix}/info

# This "Name:" SFEgcc and SFEgccruntime is a compatibility layer,
# and delivering only symbolic links to corresponding versioned
# directories with real files delivered in sub packages like 
# SFEgcc-%majorminornumber and SFEgccruntime-%majorminornumber

##TODO## make symlinks mediated symlinks for machine-local configured,
#preferred versions. Not as flexible as we want (want: user selectable
#gcc variant, but we get only whole machine defaults)

Name:		SFEgcc
IPS_package_name:	sfe/developer/gcc
Summary:	GNU gcc compiler - metapackage with symbolic links to version %{major_minor} compiler files available in %{gccsymlinks}
#Version:	see above, %{version} is set elsewhere
License:             GPLv3+
Group:		Development/C
SUNW_Copyright:      gcc.copyright
Source:              ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Patch1:              gcc-01-libtool-rpath.diff
%if %with_handle_pragma_pack_push_pop
Patch2:              gcc-02-handle_pragma_pack_push_pop.diff
%else
%endif
Patch3:              gcc-03-gnulib.diff

#LINK_LIBGCC_SPEC
#gcc-05 could be reworked to know both, amd64 and sparcv9
%ifarch i386 amd64
Patch5:              gcc-05-LINK_LIBGCC_SPEC-%{majorminornumber}.diff
%endif
%ifarch sparcv9
Patch5:              gcc-05-LINK_LIBGCC_SPEC-sparcv9-%{majorminornumber}.diff
%endif

# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=49347
# if clause to apply only on specific gcc versions, see %prep
Patch10:	gcc-10-spawn.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#Attention - this is the dependency chain for the compiler:
#      SFEgcc -needs-> SFEgcc-46,SFEgccruntime-46
# this is an example for a program which can have this
# dependency chain (most common case)
#      SFEapplication -needs-> SFEgccruntime 
# *OR* in special cases
#      SFEapplication -needs-> SFEgccruntime-46
#
# today we want exactly 4.6. later on if we can ask a minimum revision,
# then a "Requires:" can be changed to request the minimum version which
# is needed to e.g. >= 4.6
Requires:      SFEgcc-%{majorminornumber},SFEgccruntime-%{majorminornumber}
#cosmetic:
Requires:      SFEgccruntime

BuildRequires: SFElibiconv-devel
Requires:      SFElibiconv
BuildRequires: SUNWbash

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
#workaround on IPS which is wrong with BASEdir as "/" -> then assume /usr/gnu
%define SFEgmpbasedir %(pkgparam SFEgmp BASEDIR 2>/dev/null | sed -e 's+^/$+/usr/gnu+')
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

%if %SFEmpfr
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
#workaround on IPS which is wrong with BASEdir as "/" -> then assume /usr/gnu
%define SFEmpfrbasedir %(pkgparam SFEmpfr BASEDIR 2>/dev/null | sed -e 's+^/$+/usr/gnu+')
%else
BuildRequires: SUNWgnu-mpfr
Requires: SUNWgnu-mpfr
%endif

%if %SFElibmpc
BuildRequires: SFElibmpc-devel
Requires: SFElibmpc
#workaround on IPS which is wrong with BASEdir as "/" -> then assume /usr/gnu
%define SFElibmpcbasedir %(pkgparam SFElibmpc BASEDIR 2>/dev/null | sed -e 's+^/$+/usr/gnu+')
%else
#BuildRequires: empty
#Requires: empty
%endif

%if %SFEbinutils
BuildRequires: SFEbinutils
Requires: SFEbinutils
%else
BuildRequires: SUNWbinutils
Requires: SUNWbinutils
%endif

Requires: SUNWpostrun

%package -n SFEgcc-%{majorminornumber}
IPS_package_name:        sfe/developer/gcc-%{majorminornumber}
Summary:                 GNU gcc compiler - version %{major_minor} compiler files
Version:                 %{version}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}runtime-%{majorminornumber}

%package -n SFEgccruntime
IPS_package_name:        sfe/system/library/gcc-runtime
Summary:                 GNU gcc runtime libraries for applications - metapackage with symbolic links to version %{major_minor} runtime available in %{gccsymlinks}
Version:                 %{version}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}runtime-%{majorminornumber}

%package -n SFEgccruntime-%{majorminornumber}
IPS_package_name:        sfe/system/library/gcc-%{majorminornumber}-runtime        
Summary:                 GNU gcc runtime libraries for applications - version %{version} runtime library files
Version:                 %{version}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
#not apropriate Requires: %{name}

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

%if %SFElibmpc
BuildRequires: SFElibmpc-devel
Requires: SFElibmpc
%else
#BuildRequires: SUNWthis-package-not-availbale
#Requires: SUNWthis-package-not-availbale
%endif

Requires: SUNWpostrun


%if %build_l10n
%package -n SFEgcc-l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep

%if %{compat_link_usr_gnu_bin_cc}
export BAILOUTMESSAGE="\n
\n
***READ THIS***\n
\n
bailing out (%name). Consider removing those symbolic links:\n
  /usr/gnu/bin/cc and /usr/gnu/bin/cpp\n
\n
you can do this with:\n
    pfexec rm /usr/gnu/bin/cc /usr/gnu/bin/cpp\n
\n
or on recent builds, use:\n
    sudo rm /usr/gnu/bin/cc /usr/gnu/bin/cpp\n
\n
that symlink points to the gcc compiler which\n
was an error in the development version of the OS.\n
\n
See also CR 7031722 (Solaris)\n
See also Bug-ID <TBD> (OI)\n
\n
Besides that, remember to initialize your CBE environment\n
before running the pkgtool.\n
Run \"pkgtool\" with these SFE spec files only *after* initializing CBE:\n
   . /opt/dtbld/bin/env.sh\n
   pkgtool build SFEthisspec.spec\n
\n
***READ THIS***\n
\n"

/usr/bin/echo ${BAILOUTMESSAGE}

exit 1
%endif

%setup -q -c -n %{name}-%version

mkdir gcc
#with 4.3.3 in new directory libjava/classpath/
cd gcc-%{version}/libjava/classpath/
#%patch1 -p1
cd ../../..
cd gcc-%{version}
%if %with_handle_pragma_pack_push_pop
%patch2 -p1
%else
%endif
%patch3 -p1
%patch5 -p1
##TODOÃ## check versions which apply. bug says 4.3.3 is not, but 4.6.0 is
#fix maybe in 4.7.x
# if          major_minor   >=  4.4 and       major_minor   <  4.7 
%if %( expr %{major_minor} '>=' 4.4 )
%if %( expr %{major_minor} '<' 4.7 )
%patch10 -p1
%endif
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash -x," `find . -type f -name configure -exec grep -q "^#\!.*/bin/sh" {} \; -print`
#perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash -x," `find . -type f -name configure -exec grep -q "^#\!.*/bin/sh" {} \; -print`

cd gcc

%if %build_l10n
nlsopt='--with-libiconv-prefix=/usr/gnu -enable-nls'
%else
nlsopt=-disable-nls
%endif

%define ld_options      -zignore -zcombreloc -Bdirect -i

export CC=cc
export CXX=CC
export CONFIG_SHELL=/usr/bin/ksh
#maybe needed for stone old studio compilers, commented for reference
#export CPP="cc -E -Xs"
export CPP="cc -E"
export CFLAGS="-O"

export BOOT_CFLAGS="-Os -Xlinker -i %gcc_picflags %gnu_lib_path"
export BOOT_LDLAGS="%_ldflags -R%{_prefix}/%major_minor/lib %gnu_lib_path"

# for target libraries (built with bootstrapped GCC)
export CFLAGS_FOR_TARGET="-O2 -Xlinker -i %gcc_picflags"
export LDFLAGS_FOR_TARGET="%_ldflags"
export LDFLAGS="%_ldflags %gnu_lib_path"
export LD_OPTIONS="%ld_options"

# For pod2man
export PATH="$PATH:/usr/perl5/bin"

%define build_gcc_with_gnu_ld 0
#saw problems. 134 did compile, OI147 stopped with probably linker errors
##TODO## research which osbuild started to fail, adjust the number below
#%if %(expr %{osbuild} '>=' 146)
#%define build_gcc_with_gnu_ld 1
#%endif

%if %build_gcc_with_gnu_ld
export LD="/usr/gnu/bin/ld"
%else
#avoid slipping in gnu ld
#might be changed to plain /usr/bin/ld instead of CBE ld-wrapper
#export LD=`which ld-wrapper`
#it's actually better to really specify /usr/bin/ld and skip the
#extra options from the wrapper instead of ending up on a system
#without the SFE build-env and have no ld-wrapper installed there
export LD=/usr/bin/ld
%endif


../gcc-%{version}/configure			\
	--prefix=%{_prefix}			\
        --libdir=%{_libdir}			\
        --libexecdir=%{_libexecdir}		\
        --mandir=%{_mandir}			\
	--infodir=%{_infodir}			\
%if %SUNWbinutils
	--with-build-time-tools=/usr/sfw	\
	--with-as=/usr/sfw/bin/gas		\
	--with-gnu-as				\
%else
	--with-as=/usr/gnu/bin/as		\
	--with-gnu-as				\
%endif
%if %build_gcc_with_gnu_ld
	--with-ld=$LD                           \
	--with-gnu-ld				\
%else
	--with-ld=$LD                           \
	--without-gnu-ld			\
%endif
	--enable-languages=c,c++,fortran,objc	\
	--enable-shared				\
	--disable-static			\
	--enable-decimal-float			\
%if %SFEgmp
	--with-gmp=%{SFEgmpbasedir}             \
%else
        --with-gmp_include=%{_basedir}/include/gmp \
%endif
%if %SFEmpfr
	--with-mpfr=%{SFEmpfrbasedir}           \
%else
        --with-mpfr_include=%{_basedir}/include/mpfr \
%endif
%if %SFElibmpc
	--with-mpc=%{SFElibmpcbasedir}           \
%else
        --with-mpc_include=%{_basedir}/include	\
%endif
	$nlsopt

gmake -j$CPUS bootstrap-lean \
             BOOT_CFLAGS="$BOOT_CFLAGS"                  \
             CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"      \
             CXXFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"


%install
rm -rf $RPM_BUILD_ROOT

cd gcc
gmake install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

#link runtime libs, for compatibility
#note: links only "basename_of_lib", then "major"-number version libs
#leaves out "minor" and "micro" version libs, they are normally not
#to be linked by userland binaries (runtime linking, see output of "ldd binaryname")

# remove trailing slash, change to "../" and remove trailing slash again
#  OFFSET=$( echo $SYMLINKTARGET | sed -e 's?/$??' -e 's?\w*/?../?g' -e 's?\w*$??' )

for SYMLINKTARGET in %{gccsymlinks}
do
  # make from /usr/gcc this offset ../../
  OFFSET=$( echo "$SYMLINKTARGET" | sed -e 's?/$??' -e 's?\w*/?../?g' -e 's?\w*$??' -e 's?/$??' )
  # with CWD /usr/gcc/lib, an example is ../../gcc/%major_minor/lib/libgcc_s.so.1
  mkdir -p $RPM_BUILD_ROOT/$SYMLINKTARGET/lib
  cd $RPM_BUILD_ROOT/$SYMLINKTARGET/lib
  for filepath in lib/libgcc_s.so.1 lib/libgcc_s.so lib/libgfortran.so.3 lib/libgfortran.so lib/libgomp.so.1 lib/libgomp.so lib/libobjc_gc.so.2 lib/libobjc_gc.so lib/libobjc.so.2 lib/libobjc.so lib/libssp.so.0 lib/libssp.so lib/libstdc++.so.6 lib/libstdc++.so lib/libquadmath.so lib/libquadmath.so.0
  do
  [ -r $OFFSET/gcc/%major_minor/$filepath ] && ln -s $OFFSET/gcc/%major_minor/$filepath
  done #for file
done #for SYMLINKTARGET

#link arch runtime libs for compatibility
%ifarch amd64 sparcv9
for SYMLINKTARGET in %{gccsymlinks}
do
  # make from /usr/gcc this offset ../../
  OFFSET=$( echo "$SYMLINKTARGET" | sed -e 's?/$??' -e 's?\w*/?../?g' -e 's?\w*$??' -e 's?/$??' )
  # with CWD /usr/gcc/lib, an example is ../../gcc/%major_minor/lib/libgcc_s.so.1
  mkdir -p $RPM_BUILD_ROOT/$SYMLINKTARGET/lib/%{_arch64}
  cd $RPM_BUILD_ROOT/$SYMLINKTARGET/lib/%{_arch64}
  for filepath in lib/%{_arch64}/libgcc_s.so.1 lib/%{_arch64}/libgcc_s.so lib/%{_arch64}/libgfortran.so.3 lib/%{_arch64}/libgfortran.so lib/%{_arch64}/libgomp.so.1 lib/%{_arch64}/libgomp.so lib/%{_arch64}/libobjc.so.2 lib/%{_arch64}/libobjc.so lib/%{_arch64}/libssp.so.0 lib/%{_arch64}/libssp.so lib/%{_arch64}/libstdc++.so.6 lib/%{_arch64}/libstdc++.so lib/%{_arch64}/libquadmath.so lib/%{_arch64}/libquadmath.so.0
  do
  #note add one ../ for %{_arch64}
  [ -r $OFFSET/../gcc/%major_minor/$filepath ] && ln -s $OFFSET/../gcc/%major_minor/$filepath
  done #for file
done #for SYMLINKTARGET
%endif

for SYMLINKTARGET in %{gccsymlinks}
do
  # make from /usr/gcc this offset ../../
  OFFSET=$( echo "$SYMLINKTARGET" | sed -e 's?/$??' -e 's?\w*/?../?g' -e 's?\w*$??' -e 's?/$??' )
  # with CWD /usr/gcc/lib, an example is ../../gcc/%major_minor/lib/libgcc_s.so.1
  mkdir -p $RPM_BUILD_ROOT/$SYMLINKTARGET/bin
  cd $RPM_BUILD_ROOT/$SYMLINKTARGET/bin
# leave out sfw gcc 3.x.x uses this name already ln -s ../../gcc/%major_minor/bin/cpp
  for filepath in bin/c++ bin/g++ bin/gcc bin/gcov bin/gfortran
  do
  [ -r $OFFSET/gcc/%major_minor/$filepath ] && ln -s $OFFSET/gcc/%major_minor/$filepath
  done #for file
done #for SYMLINKTARGET

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
%ifarch amd64 sparcv9
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.la
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%post -n SFEgcc
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun -n SFEgcc
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE



#SFEgcc-%{majorminornumber}, other packages see below

%files -n SFEgcc-%{majorminornumber}
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gcc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*.7
%{_infodir}
%{_includedir}

%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}
%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}/python
%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}/python/libstdcxx
%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}/python/libstdcxx/v6
%{_datadir}/gcc-%{version}/python/libstdcxx/v6/printers.py
%{_datadir}/gcc-%{version}/python/libstdcxx/v6/__init__.py
%{_datadir}/gcc-%{version}/python/libstdcxx/__init__.py


%files -n SFEgccruntime-%{majorminornumber}
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.spec
%ifarch amd64 sparcv9 i386
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/lib*.spec
%endif

%if %symlinktarget1enabled
%files -n SFEgcc
%defattr (-, root, bin)
%{symlinktarget1path}/bin
%files -n SFEgccruntime
%defattr (-, root, bin)
%{symlinktarget1path}/lib
%endif

%if %symlinktarget2enabled
%files -n SFEgcc
%defattr (-, root, bin)
%{symlinktarget2path}/bin
%files -n SFEgccruntime
%defattr (-, root, bin)
%{symlinktarget2path}/lib
%endif

%if %symlinktarget3enabled
%files -n SFEgcc
%defattr (-, root, bin)
%{symlinktarget3path}/bin
%files -n SFEgccruntime
%defattr (-, root, bin)
%{symlinktarget3path}/lib
%endif


%if %build_l10n
%files -n SFEgcc-l10n
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Jun 22 2012 - Thomas Wagner
- back to CC=cc and CXX=CC as solarisstudio is still needed for SFE anyways.
  and that way we don't need gcc-3 installed generally. Maybe the wrong
  symlink /usr/gnu/bin/cc missled to use CC=gcc before.
- changed back CPP to run solarisstudio and not gcc, removed "-Xs" as it looks
  like not longer needed, now it is CPP="cc -E"
- Removed BuildRequires: SUNWgcc  (which is gcc-3 on IPS)
- make a bail-out mechanism if user still has poisonous symlinks /usr/gnu/bin/cc
  and /usr/gnu/bin/cpp. They need to be removed to avoid breakage for some
  build systems ignoring $PATH variable (set by CBE to first find "cc" as
  the solaristudio compiler)
* Thu Jun 21 2012 - Logan Bruns <logan@gedanken.org>
- Replaced CPP="cc -E -Xs" with CPP="gcc -E"
* Wed Jun 20 2012 - Thomas Wagner
- automate transform of version number to string for package names e.g. SFEgcc-46
- apply Patch 10 spawn as well for other versions 4.6 and higher, fixes build 4.5 (no spawn patch)
- prepare fresh patches for LINK_LIBGCC_SPEC for 4.7.x/4.6.x/4.7.x
  use %{majorminornumber} to match the right filename,
  old patch name gcc-05-LINK_LIBGCC_SPEC.diff will remain because external 
  documentation links to this filename!
* Sat Mar 03 2012 - Milan Jurik
- bump to 4.6.3
* Wed Dec 23 2011 - Milan Jurik
- add libquadmath symlinks
* Sun Dec 04 2011 - Milan Jurik
- patch10 for spawn issue
* Sat Oct 29 2011 - Milan Jurik
- bump to 4.6.2
* Thr Oct 13 2011 - Thomas Wagner
- add to LDFLAGS %gnu_lib_path or cc1 can't find libs in bootstrapping the compiler
- remove typo in LDFLAGS_FOR_TARGET="%_ldflags"
* Wed Oct 11 2011 - Thomas Wagner
- add IPS_package_names
- little cleaning up: remove development comments
* Tue Sep 27 2011 - Thomas Wagner
- add version control form outside, so you can build and version
  (if the patches apply cleanly). Note: only one micro version at
  a time is supported by the naming schema: 4.6.1 -> SFEgcc-46
  4.5.3 -> SFEgcc-45, and not at the same time 4.5.2 -> SFEgcc-45.
  Always send to the repo last, what then should be the version
  providing the symlinks in /usr/gnu/<bin|lib>
  e.g. first 4.5.3 then second 4.6.1 -> you get SFEgcc symlinks to 4.6.1 version
* Thu Sep 22 2011 - Thomas Wagner
- automate symlinks to be created in for instance /usr/gnu/bin or /usr/gcc/bin
  as requested at compile time by the configure line --enable-languages=c,c++,fortran,objc
  This works automaticly and independent of number of languages enabled
- reverse package odering, make filename match package SFEgcc, this fixes --autodeps
##TODO## review/verify documentatioin in patch gcc-03-gnulib.diff
- document patch gcc-03-gnulib.diff backgrounds
##TODO## review/verify documentatioin in patch gcc-05-LINK_LIBGCC_SPEC.diff
- add patch gcc-05-LINK_LIBGCC_SPEC.diff (inspired by pkgsrc's gcc variant!)
  to make gcc always know where the gcc compiler runtime lives. Needed to get
  rid of excessive number of directories hardcoded in -R  (patch gcc-03-gnulib.diff
  new version removed them, resultingin libgcc_s.so and libstdc++.so.6 not always
  found). Only downside: if you want a user library then really *do* specify one
  -R/usr/gnu/lib for instance. Else find a clean binary with the correct runpath
- move %gnu_lib_path over from LDFLAGS + LD_OPTIONS to BOOT_CFLAGS, removes 
  excessive number of directories in runpath of binaries, but still finds iconv, 
  mpfr, gmp, mpc in /usr/gnu/lib at compiler bootstrap and when using the compiler 
  itself.
- second draft of a compile time selectable set of target directories where
  gcc symlinks for compiler and runtime are support to going to. Current 
  simplification is that all symlinks go into a single target package SFEgcc 
  respectively SFEgccruntime.
- avoid slipping in gnu-ld with the new consolidation of /usr/sfw/bin/<ld|*> and/or
  /usr/ccs/bin over to /usr/bin which might be accidentially be the first in PATH.
  Set LD=`which ld-wrapper`   -->> NOTE changd again later
- it's actually better to really specify LD=/usr/bin/ld then specifying 
  eventually unavailable ld-wrapper script (in case CBE is not installed)
- make extra matapackages available to be set as "Requires:" in consumer packages
  and add packages which version number in theyr names that can will be pulled 
  in by the metapackages or consumer packages. In selected special cases
  programs can "Requires:" the versioned SFEgccruntime-46 package name.
- first draft patch5 gcc-05-LINK_LIBGCC_SPEC-sparcv9.diff for sparcv9 - needs
  testing, please give feedback
* Tue Aug 16 2011 - Thomas Wagner
- first version of reworked gcc-03-gnulib.diff where user can
  define libdirs everywhere in RUNPATH, e.g. /usr/g++/lib:/usr/gnu/lib:/usr/lib
  please test results with  dump -Lv /usr/g++/lib/libQtNetwork.so | grep RUNPATH
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jul 17 2011 - Alex Viskovatoff
- do not hardcode <majornumber>.<minornumber>
* Sun Jul 17 2011 - Milan Jurik
- bump to 4.6.1
* Tue May 17 2011 - Milan Jurik
- bump to 4.5.3
* Thu Mar 17 2011 - Thomas Wagner
- temporarily force SFEgmp SFEmpfr to have pkgtool --autodeps working in correct build-order
* Wed Mar 16 2011 - Thomas Wagner
- symlinks did not go into package, added %{_gnu_bindir}/* to %files SFEgcc 
* Tue Mar 15 2011 - Thomas Wagner
- add missing %define _gnu_bindir %{_basedir}/gnu/bin
* Sat Mar 12 2011 - Thomas Wagner
- make symlinks to get SFEgcc.spec version 4.x.x to have the gcc 4.x.x
  default compiler accessible by /usr/gnu/bin/gcc and /usr/gnu/bin/g++ 
  and /usr/gnu/bin/gfortran ...
* Fri Mar 04 2011 - Milan Jurik
- RUNPATH enforced to contain /usr/gnu/lib, libs symlinked to /usr/gnu/lib
* Wed Mar 02 2011 - Milan Jurik
- fix NLS build, need to fix linker for g++ still
* Tue Mar 01 2011 - Milan Jurik
- move to /usr/gcc/4.5
* Tue Feb 08 2011 - Thomas Wagner
- interim solution for very old gcc-4.3.3, derived from experimental/SFEgcc-4.5.2.spec
* Sun Jan 30 2011 - Thomas Wagner
- bump to 4.5.2
* Sat Oct 23 2010 - Thomas Wagner
- bump to 4.5.1
- require SFEgmp / SFEmpfr (new version) for builds below 126. may add
  upper limit later if OS contains required version as SUNWgnu-mp / SUNWgnu-mpfr
- finetune BASEDIR detection (SVR4 works, IPS lacks BASEDIR -> emulate)
- merge new logic for (Build)Requires from SFEgcc version 4.4.4 to 4.5.0 spec file
- start with osbuild >= 146 to use gnu ld for linking (build_gcc_with_gnu_ld)
  because looks like linker error
- collect python files from directory based on gcc %version
- make spec bailout if the symlink /usr/gnu/bin/cc exists
- add (Build)Requires SFElibmpc.spec  (SFEMpc might retire, naming)
- add new python files to %files
- add experimental --with-SFEbinutils to force using more fresh SFEbinutils
- don't hard-code ld-wrapper location, use instead `which ld-wrapper`
* Mon Jul 28 2010 - Thomas Wagner
- bump to 4.5.0
* Wed Aug 18 2010 - Thomas Wagner
- try with defaults to SUNWbinutils SUNWgnu-mp SUNWgnu-mpfr
  this might break gcc compile on older osbuild versions
- stop and exit 1 if the link /usr/gnu/bin/cc exists. Give user hint to 
  remove this problematic symlink of gcc to cc
- search ld-wrapper from PATH (e.g. /opt/jdsbld/bin or /opt/dtbld/bin)
- workaround IPS bug that ever prints BASEdir as "/" even if it presents 
  "/usr/gnu" to have configure find SFEgmp and SFEmpfr in case it should 
* Sun Jun  6 2010 - Thomas Wagner
- bump to 4.4.4
- add switches to force SFEgmp and SFEmpfr
- experimenting with gcc related CFLAGS/LDFLAGS
* Fri Feb 05 2010 - Albert Lee <trisk@opensolaris.org>
- Fix bootstrap compiler options
* Sun Aug 09 2009 - Thomas Wagner
- BuildRequires: SUNWbash
* Sat Mar 14 2009 - Thomas Wagner
- change logic to require SFEgmp/SFEmpfr only if *no* SUNWgnu-mp/SUNWgnu-mpfr is present (this is on old OS builds)
- make SFEgcc use of new SUNWgnu-mp/SUNWgnu-mpfr (replacement for SFEgmp/SFEmpfr, SFE-versions still work with SFEgcc)
- detect new location of SFEgmp/SFEmpfr now in /usr/gnu and use them only if missing SUNWgnu-mp/SUNWgnu-mpfr
- add (Build)Requires: SFElibiconv(-devel) (thanks to check-deps.pl)
* Sat Feb 21 2009 - Thomas Wagner
- bump to 4.3.3
- make conditional SFEgmp  / SUNWgnu-mp
- make conditional SFEmpfr / SUNWgnu-mpfr
- add extra configure switch if SUNWgnu-mp and/or SUNWgnu-mpfr is used
* Sun Jan 25 2009 - Thomas Wagner
- make default without HANDLE_PRAGMA_PACK_PUSH_POP. switch on with:
  --with-handle_pragma_pack_push_pop
* Sat Jan 24 2009 - Thomas Wagner
- add HANDLE_PRAGMA_PACK_PUSH_POP (might help wine)
- bump to 4.2.4, version SFEgcc wit %{version}
* Wed Jan  7 2009 - Thomas Wagner
- add conditional SUNWbinutils/SFEbinutils to SFEgcc package
* Sun Dec 28 2008 - Thomas Wagner
- work around %files section on i386/32-bit not finding %{_arch64} binaries because _arch64 is unset ... _arch64 only set if running 64-bit OS in include/arch64.inc
* Sat Dec 27 2008 - Thomas Wagner
- add conditional SUNWbinutils/SFEbinutils to re-enable build on old OS
- add configure-switch for SUNWbinutils otherwise left over SFEbinutils catched by configure/compile. SUNWbinuils not found otherwise.
* Wed Aug 06 2008 - andras.barna@gmail.com
- change SFEbinutils to SUNWbinutils, defaulting to SUN ld
* Mon Mar 10 2008 - laca@sun.com
- add missing defattr
* Sun Mar  2 2008 - Mark Wright <markwright@internode.on.net>
- Add gcc-01-libtool-rpath.diff patch for a problem where
- the old, modified libtool 1.4 in gcc 4.2.3 drops
- -rpath /usr/gnu/lib when building libstdc++.so.6.0.9.
* Fri Feb 29 2008 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.3.  Remove patch for 32787 as it is upstreamed into gcc 4.2.3.
* Sat Jan 26 2008 - Moinak Ghosh <moinak.ghosh@sun.com>
- Refactor package to have SFEgcc and SFEgccruntime.
* Sun Oct 14 2007 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.2.
* Wed Aug 15 2007 - Mark Wright <markwright@internode.on.net>
- Change from /usr/ccs/bin/ld to /usr/gnu/bin/ld, this change
  requires SFEbinutils built with binutils-01-bug-2495.diff,
  binutils-02-ld-m-elf_i386.diff and binutils-03-lib-amd64-ld-so-1.diff.
  Add objc to --enable-languages, add --enable-decimal-float.
* Wed Jul 24 2007 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.1, add patch for gcc bug 32787.
* Wed May 16 2007 - Doug Scott <dougs@truemail.co.th>
- Bump to 4.2.0
* Tue Mar 20 2007 - Doug Scott <dougs@truemail.co.th>
- Added LD_OPTIONS so libs in /usr/gnu/lib will be found
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- change to use GNU as from SFEbinutils
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
