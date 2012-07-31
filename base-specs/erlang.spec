#
# spec file for package: erlang
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

Name:		erlang
Version:	14.2.3
Source0:	http://www.erlang.org/download/otp_src_R14B03.tar.gz
Patch0:		erlang-01-hwaddr.diff
Patch1:		erlang-02-int-typedef.diff
Patch2:		erlang-03-erl_gl-linker.diff

%prep
%setup -q -n otp_src_R14B03
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i -e 's,$rdir/include,$rdir/include/odbc,g' lib/odbc/configure lib/odbc/configure.in
sed -i -e 's,${libdir}/64,${libdir}/%{_arch64},g' lib/odbc/configure lib/odbc/configure.in

%build
export CC=/usr/gcc/bin/gcc
export CXX=/usr/gcc/bin/g++
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{myldflags}"
./configure --prefix=%{_prefix} --bindir=%{mybindir} --libdir=%{_libdir} --with-wx-config=%{wx_config}
make

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT
