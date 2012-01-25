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
Version:	3.4.0
Source:		ftp://ftp.netlib.org/lapack/lapack-%{version}.tgz
Patch1:		lapack-01-fpic.diff
Group:		Math
URL:		http://www.netlib.org/lapack/

%prep
%setup -q -c -n %{name}
cd lapack-%{version}
%patch1 -p1

%build
cd lapack-%{version}
mv make.inc.example make.inc
ln -s %{_libdir}/libblas.a blas.a
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
  make F77=f77 FORTRAN=f90 LOADER=f90 PLAT="" OPTS="-O3 -m64" \
       LOADOPTS=-m64 NOOPT="-O0 -m64"
else
  # Adding fPIC here does nothing. Patch will manually fix makefile.
  #make F77=gortran FORTRAN=gfortran PLAT="" OPTS="-O3 -fPIC" \
  #     NOOPT="-O0 -fPIC"

  # Now, build blaslib first to prevent possible compile hiccup
  make blaslib
  make
fi

%install
cd lapack-%{version}
install -d -m 0755 $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 liblapack.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Jan 17 2012 - James Choi
- Bump to 3.4.0, specify fPIC
* Tue May 25 2010 - Milan Jurik
- disable multiarch support, not stable with Sun studio Fortran and unsupported with gfortran yet
* Mon May 24 2010 - Milan Jurik
- multiarch support
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
