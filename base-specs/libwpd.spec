#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:	libwpd
Version:	0.9.4
Source:	%{sf_download}/%{name}/%{name}-%{version}.tar.bz2

%prep
%setup -q

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%if %cc_is_gcc
export CC=gcc
export CXX=g++
%endif

export CFLAGS="%optflags"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}	\
	--libdir=%{_libdir}	\
	--mandir=%{_mandir}	\
	--enable-shared=yes	\
	--enable-static=no	\
	--with-pic		\
	--disable-werror

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Dec 29 2011 - Milan Jurik
- multiarch support
