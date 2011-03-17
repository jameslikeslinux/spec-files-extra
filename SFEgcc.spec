#
# spec file for package SFEgcc
#
# includes module(s): GNU gcc
#

##NOTE## This spec file is an interim solution regarding the path layout on disk
##       expect relocation to /usr/gcc/4.5/ and symlinks provided from /usr/gnu 
##       into to that location (provided by the latest installed or "pkg fix"ed gcc-45 
##NOTE## most likely the package name will change to SFEgcc-43 and another empty
##       package SFEgcc will be created always requiring the latest SFEgcc-<major><minor>
##NOTE## If you experience problems with that version bump, please drop us a note
##NOTE## you will need "pkg uninstall SFEgccruntime and SFEgcc" *before* you can
#        to get this spec build successfully. Reason: older runtime-libs interfere
#        with building this eventually incompatible, newer gcc runtime from this spec


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

%define _prefix /usr/gcc/4.5
%define _infodir %{_prefix}/info
%define _gnu_bindir %{_basedir}/gnu/bin
%define _gnu_libdir %{_basedir}/gnu/lib

Name:                SFEgccruntime
Summary:             GNU gcc runtime libraries required by applications
Version:             4.5.2
Source:              ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Patch1:              gcc-01-libtool-rpath.diff
%if %with_handle_pragma_pack_push_pop
Patch2:              gcc-02-handle_pragma_pack_push_pop.diff
%else
%endif
Patch3:              gcc-03-gnulib.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

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

%package -n SFEgcc
Summary:                 GNU gcc
Version:                 %{version}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

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

export CC=gcc
export CXX=g++
#export CONFIG_SHELL=/usr/bin/bash
export CONFIG_SHELL=/usr/bin/ksh
export CPP="cc -E -Xs"
export CFLAGS="-O"
# for stage2 and stage3 GCC
#export BOOT_CFLAGS="%gcc_optflags -Os -Xlinker -i %gcc_picflags"
#-m64 and i586 mutually exclusive
export BOOT_CFLAGS="-Os -Xlinker -i %gcc_picflags"
# for target libraries (built with bootstrapped GCC)
#export CFLAGS_FOR_TARGET="%gcc_optflags -O2 -Xlinker -i %gcc_picflags"
#-m64 and i586 mutually exclusive
export CFLAGS_FOR_TARGET="-O2 -Xlinker -i %gcc_picflags"
export LDFLAGS="%_ldflags %gnu_lib_path"
export LD_OPTIONS="%ld_options %gnu_lib_path"
#export LD_LIBRARY_PATH="%gnu_lib_path"

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
	--with-ld=/usr/gnu/bin/ld		\
	--with-gnu-ld				\
%else
	--with-ld=`which ld-wrapper`     \
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

make -j$CPUS bootstrap-lean BOOT_CFLAGS="$BOOT_CFLAGS" CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET" CXXFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"

%install
rm -rf $RPM_BUILD_ROOT

cd gcc
make install DESTDIR=$RPM_BUILD_ROOT

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
mkdir -p $RPM_BUILD_ROOT%{_gnu_libdir}
cd $RPM_BUILD_ROOT%{_gnu_libdir}
ln -s ../../gcc/4.5/lib/libgcc_s.so.1
ln -s ../../gcc/4.5/lib/libgcc_s.so
ln -s ../../gcc/4.5/lib/libgfortran.so.3
ln -s ../../gcc/4.5/lib/libgfortran.so
ln -s ../../gcc/4.5/lib/libgomp.so.1
ln -s ../../gcc/4.5/lib/libgomp.so
ln -s ../../gcc/4.5/lib/libobjc_gc.so.2
ln -s ../../gcc/4.5/lib/libobjc_gc.so
ln -s ../../gcc/4.5/lib/libobjc.so.2
ln -s ../../gcc/4.5/lib/libobjc.so
ln -s ../../gcc/4.5/lib/libssp.so.0
ln -s ../../gcc/4.5/lib/libssp.so
ln -s ../../gcc/4.5/lib/libstdc++.so.6
ln -s ../../gcc/4.5/lib/libstdc++.so
#link arch runtime libs for compatibility
%ifarch amd64 sparcv9
mkdir -p $RPM_BUILD_ROOT%{_gnu_libdir}/%{_arch64}
cd $RPM_BUILD_ROOT%{_gnu_libdir}/%{_arch64}
ln -s ../../../gcc/4.5/lib/%{_arch64}/libgcc_s.so.1
ln -s ../../../gcc/4.5/lib/%{_arch64}/libgcc_s.so
ln -s ../../../gcc/4.5/lib/%{_arch64}/libgfortran.so.3
ln -s ../../../gcc/4.5/lib/%{_arch64}/libgfortran.so
ln -s ../../../gcc/4.5/lib/%{_arch64}/libgomp.so.1
ln -s ../../../gcc/4.5/lib/%{_arch64}/libgomp.so
#ln -s ../../../gcc/4.5/lib/%{_arch64}/libobjc_gc.so.2
#ln -s ../../../gcc/4.5/lib/%{_arch64}/libobjc_gc.so
ln -s ../../../gcc/4.5/lib/%{_arch64}/libobjc.so.2
ln -s ../../../gcc/4.5/lib/%{_arch64}/libobjc.so
ln -s ../../../gcc/4.5/lib/%{_arch64}/libssp.so.0
ln -s ../../../gcc/4.5/lib/%{_arch64}/libssp.so
ln -s ../../../gcc/4.5/lib/%{_arch64}/libstdc++.so.6
ln -s ../../../gcc/4.5/lib/%{_arch64}/libstdc++.so
%endif

#link binaries into usual place the former SFEgcc used and 
#a lot of spec files still use and are as well the recommended
#paths to specify just what the "default" SFEgcc 4-series
#compiler is called from. Note: binaries built that way *may*
#point to libraries found in a compiler major.minor specific
#directory in /usr/gcc/<majornumber>.<minornumber> 
#This is in preparation for eventually getting a meta-level
#package SFEgcc (contains symlinks only into /usr/gcc/<majornumber>.<minornumber>,
#and is the package Requirement written in customer spec files.
#below that SFEgcc packages, a SFEgcc-452 exists with the real compiler in it

#NOTE: the os-distro delivers the "SFW" version of gcc 3.x.x
#and therefore does deliver links into /usr/gnu/bin:
#/usr/gnu/bin/cc    ->    ../../sfw/bin/gcc     (stays)
#/usr/gnu/bin/cpp   ->    ../../sfw/bin/cpp     (stays, interferes with us)
#we do exclude "cpp" from this SFEgcc.spec for that reason!

#link binaries, enables CC=/usr/gnu/bin/gcc CXX=/usr/gnu/bin/g++ 
#to get SFEgcc.spec version 4.x compiler in use without specifying
#the exact SFEgcc compiler version number, just use the most recent 4.x.x
mkdir -p $RPM_BUILD_ROOT%{_gnu_bindir}
cd $RPM_BUILD_ROOT%{_gnu_bindir}
ln -s ../../gcc/4.5/bin/c++
# leave out sfw gcc 3.x.x uses this name already ln -s ../../gcc/4.5/bin/cpp
ln -s ../../gcc/4.5/bin/g++
ln -s ../../gcc/4.5/bin/gcc
ln -s ../../gcc/4.5/bin/gccbug
ln -s ../../gcc/4.5/bin/gcov
ln -s ../../gcc/4.5/bin/gfortran
#most likely not needed are those, you can specify in your spec file
#/usr/gcc/4.5/bin/i386-pc-solaris2.11-* if you really want
#ln -s ../../gcc/4.5/bin/i386-pc-solaris2.11-c++
#ln -s ../../gcc/4.5/bin/i386-pc-solaris2.11-g++
#ln -s ../../gcc/4.5/bin/i386-pc-solaris2.11-gcc
#ln -s ../../gcc/4.5/bin/i386-pc-solaris2.11-gcc-4.5.2
#ln -s ../../gcc/4.5/bin/i386-pc-solaris2.11-gfortran

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

%files
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
%{_gnu_libdir}


%files -n SFEgcc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_gnu_bindir}
%{_gnu_bindir}/*
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

%if %build_l10n
%files -n SFEgcc-l10n
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
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
