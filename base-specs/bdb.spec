#
# spec file for package bdb
#
# includes module(s): bdb
#

Name:		bdb
Summary:	Berkeley DB
Group:		System/Databases
Version:	4.8.30
License:        BSD3c
Source:		http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
URL:		http://www.oracle.com/technology/software/products/berkeley-db/index.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n db-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags}"
cd build_unix
../dist/configure                           \
        --prefix=%{_prefix}                 \
        --bindir=%{_bindir}                 \
        --libdir=%{_libdir}                 \
        --libexecdir=%{_libexecdir}         \
        --mandir=%{_mandir}                 \
        --datadir=%{_datadir}               \
        --infodir=%{_datadir}/info          \
	--enable-compat185		    \
        --disable-static                    \
        --enable-shared



make -j$CPUS 

%install
cd build_unix
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
#rm $RPM_BUILD_ROOT%{_libdir}/*.a
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/doc
mv $RPM_BUILD_ROOT%{_prefix}/docs $RPM_BUILD_ROOT%{_prefix}/share/doc/bdb

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Aug 28 2012 - Milan Jurik
- support multiarch
