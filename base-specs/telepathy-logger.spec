#
# spec file for package telepathy-logger
#
# Owner:yippi
#

Name:           telepathy-logger
License:        GPL
Group:          Applications/Internet
Version:        0.4.0
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Summary:        IM backend
Source:		http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.bz2
Patch1:         telepathy-logger-01-configure.diff
URL:            http://developer.pidgin.im/wiki/Telepathy
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/telepathy-haze

Autoreqprov: on
Prereq:      /sbin/ldconfig

%description
A connection manager based on libpurple, bringing support for Pidgin's IM
protocols to the Telepathy framework.

%prep
%setup -q
%patch1 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

autoconf 
CFLAGS="$RPM_OPT_FLAGS"			        \
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libexecdir}/*
%{_datadir}/doc/*

%changelog
* Thu May 10 2012 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 0.4.0.
* Wed Jul 06 2011 - Brian Cameron <brian.cameron@oracle.com>
- Created with version 0.2.10.
