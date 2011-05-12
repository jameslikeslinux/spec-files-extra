#
# spec file for package ossp-uuid
#
# includes module(s): ossp-uuid
#

Name:                    ossp-uuid
Summary:                 API and CLI for Universally Unique Identifiers from OSSP
Version:                 1.6.2
Source:                  http://ftp.netbsd.org/pub/NetBSD/packages/distfiles/uuid-%{version}.tar.gz
Patch1:                  ossp-uuid-01-debian-0001.diff
Patch2:                  ossp-uuid-02-debian-0002.diff
Patch3:                  ossp-uuid-03-ldflags.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n uuid-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags" 
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    export LDFLAGS="$LDFLAGS -m64"
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --enable-shared		     \
	    --disable-static

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu May 12 2011 - Albert Lee <trisk@opensolaris.org>
- Initial base spec
