#
# spec file for package lapack
#
# includes module(s): lapack
#

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:		lapack
Summary:	LAPACK - Linear Algebra PACKage
Version:	3.4.2
Source:		http://www.netlib.org/lapack/lapack-%{version}.tgz
Group:		Math
URL:		http://www.netlib.org/lapack/
#patches taken from Fedora
#http://pkgs.fedoraproject.org/gitweb/?p=lapack.git
Patch1:		lapack-3.4.0-make.inc.patch
Patch2:		lapack-3.4.1-lapacke.patch
Patch3:		lapack-3.4.0-xblas.patch
Source1:	Makefile.blas
Source2:	Makefile.lapack

%prep
%setup -q -c -n %{name}
cd lapack-%{version}
cp -f INSTALL/make.inc.gfortran make.inc
cp -f %SOURCE1 BLAS/SRC/Makefile
cp -f %SOURCE2 SRC/Makefile
%patch1 -p1
%patch2 -p0
%patch3 -p0

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd lapack-%{version}
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
  make F77=f77 FORTRAN=f90 LOADER=f90 PLAT="" OPTS="-O3 -m64" \
       LOADOPTS=-m64 NOOPT="-O0 -m64"
else
  pushd BLAS/SRC
  gmake -j$CPUS NOOPT="-O0 -fPIC" F77=gfortran FORTRAN=gfortran PLAT="" OPTS="-O3 -fPIC" shared
  gmake -j$CPUS NOOPT="-O0 -fPIC" F77=gfortran FORTRAN=gfortran PLAT="" OPTS="-O3 -fPIC" static
  popd

  cp BLAS/SRC/libblas.* .

  pushd INSTALL
  gmake clean
  gmake -j$CPUS NOOPT="-fPIC" F77=gfortran FORTRAN=gfortran PLAT="" OPTS="-O3 -fPIC"
  popd

  pushd SRC
  gmake clean
  gmake -j$CPUS NOOPT="-O0 -fPIC" FFLAGS="-fPIC" CFLAGS="-fPIC" F77=gfortran FORTRAN=gfortran PLAT="" OPTS="-O3 -fPIC" shared
  gmake -j$CPUS NOOPT="-O0 -fPIC" F77=gfortran FORTRAN=gfortran PLAT="" OPTS="-O3 -fPIC" static
  popd

  cp SRC/liblapack.* .

  pushd lapacke
  gmake clean
  gmake -j$CPUS F77=gfortran FORTRAN=gfortran PLAT="" OPTS="-O3 -fPIC" CFLAGS="-O3 -fPIC"
  popd


fi

%install
cd lapack-%{version}
install -d -m 0755 $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 liblapack.so $RPM_BUILD_ROOT%{_libdir}
install -m 0755 liblapacke.so $RPM_BUILD_ROOT%{_libdir}
install -m 0755 libblas.so $RPM_BUILD_ROOT%{_libdir}
install -m 0755 liblapack.a $RPM_BUILD_ROOT%{_libdir}
install -m 0755 liblapacke.a $RPM_BUILD_ROOT%{_libdir}
install -m 0755 libblas.a $RPM_BUILD_ROOT%{_libdir}


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 26 2012 - Logan Bruns <logan@gedanken.org>
- bump to 3.4.2
* Sun Jun 10 2012 - Pavel Heimlich
- update source url
* Mon Apr 30 2012 - Pavel Heimlich
- make shared libraries
* Tue Jan 17 2012 - James Choi
- Bump to 3.4.0, specify fPIC
* Tue May 25 2010 - Milan Jurik
- disable multiarch support, not stable with Sun studio Fortran and unsupported with gfortran yet
* Mon May 24 2010 - Milan Jurik
- multiarch support
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
