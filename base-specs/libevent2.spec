#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:		libevent2
Summary:	An event notification library for event-driven network servers.
Version:	2.0.15
Source:		%sf_download/levent/libevent/libevent-2.0/libevent-%version-stable.tar.gz
URL:		http://monkey.org/~provos/libevent/
Group:		System/Libraries

%prep
%setup -q -n libevent-%version-stable

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}	\
	--libdir=%{_libdir}	\
	--mandir=%{_mandir}	\
	--docdir=%_docdir	\
	--disable-static

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libevent*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Nov 17 2011 - Milan Jurik
- multiarch support
