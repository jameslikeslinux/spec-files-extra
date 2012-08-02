# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:		protobuf
Summary:	Protocol Buffers library
Version:	2.4.1
URL:		https://code.google.com/p/protobuf/
Source:		http://protobuf.googlecode.com/files/%{name}-%{version}.tar.bz2
Group:		System/Libraries
License:	BSD
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
%include default-depend.inc

%description
Protocol Buffers are a way of encoding structured data in an efficient yet extensible format. Google uses Protocol Buffers for almost all of its internal RPC protocols and file formats.

%prep
%setup -q -n %{name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
./configure --prefix=%{_prefix} \
	--enable-shared		\
	--disable-static
else
./configure --prefix=%{_prefix} \
	--enable-shared		\
	--disable-static	\
	--disable-64bit-solaris
fi

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue May 01 2012 - Milan Jurik
- Initial spec
