#
# spec file for package libmpc
#
# includes module(s): GNU mpc
#

%define SFEgmp  %(/usr/bin/pkginfo -q SFEgmp && echo 1 || echo 0)
%define SFEmpfr %(/usr/bin/pkginfo -q SFEmpfr && echo 1 || echo 0)

##TODO## think on usr-gnu.inc define infodir inside /usr/gnu/share to avoid conflicts
%define _infodir	%{_datadir}/info

Name:		mpc
Version:	0.8.2
Summary:	C library for for the arithmetic of complex numbers with arbitrarily high precision and correct rounding of the result
URL:		http://www.multiprecision.org/mpc/
Source:		http://www.multiprecision.org/mpc/download/mpc-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build


%prep
%setup -q

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%{optflags} -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path}"

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}			\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --enable-shared			\
	    --disable-static			\
%if %SFEgmp
            --with-gmp=%{SFEgmpbasedir}         \
%else
            --with-gmp-include=%{_basedir}/include/gmp	\
%endif
%if %SFEmpfr
            --with-mpfr=%{SFEmpfrbasedir}	\
%else
            --with-mpfr-include=%{_basedir}/include/mpfr	\
%endif
	    $nlsopt

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Mar 01 2011 - Milan Jurik
- start proper multiarch
