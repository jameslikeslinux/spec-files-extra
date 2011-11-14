#
# Copyright (c) 2011 Oracle Corporation
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp g++
%include base.inc

Name:                SFElighttpd
Summary:             Lighttpd Web Server
IPS_package_name:    web/server/lighttpd-14
Version:             1.4.29
Source:              http://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-%{version}.tar.gz 
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWpcre
Requires: SUNWpcre

%prep
%setup -q -n lighttpd-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --with-openssl=/usr --with-attr --with-fam --with--gdbm \
            --with-kerberos5 --with-ldap --with-lua --with-memcache \
	    --with-mysql=/usr/mysql/5.1/bin/mysql_config \
	    --with-pcre --with-webdav-locks --with-webdav-props

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/mod_*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/lighttpd
%{_sbindir}/lighttpd-angel
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/mod*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man8/*.8

%changelog
* Fri Oct 16 2011 - Ken Mays <kmays2000@gmail.com>
- Updated for MySql 5.1 package.
* Fri Oct 14 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.4.29
* Wed May 14 2008 - Ananth Shrinivas <ananth@sun.com>
- Lighty has moved light years ahead. Bump to 1.4.19 
* Sun Mar 04 2007 - Eric Boutilier
- Initial spec
