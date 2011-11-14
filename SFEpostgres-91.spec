#
# spec file for package PostgreSQL 9.0
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc
%include packagenamemacros.inc

%define _prefix /usr/postgres
%define _var_prefix /var/postgres
%define tarball_name     postgresql
%define tarball_version  9.1.1
%define major_version	 9.1

%define _basedir         %{_prefix}/%{major_version}

Name:                    SFEpostgres-91
IPS_package_name:        database/postgres-91
Summary:	         PostgreSQL client tools
Version:                 9.1.1
License:		 PostgreSQL
Url:                     http://www.postgresql.org/
Source:			 http://wwwmaster.postgresql.org/redir/311/h/source/v%{tarball_version}/%{tarball_name}-%{tarball_version}.tar.bz2
Source1:		 postgres-91-postgres_91
Source2:		 postgres-91-postgresql_91.xml
Source3:		 postgres-91-auth_attr
Source4:		 postgres-91-prof_attr
Source5:		 postgres-91-exec_attr
Source6:		 postgres-91-user_attr
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: %{pnm_buildrequires_SUNWlxsl}
BuildRequires: %{pnm_buildrequires_SUNWlxml}
BuildRequires: %{pnm_buildrequires_SUNWgss}
BuildRequires: %{pnm_buildrequires_SUNWopenssl}
BuildRequires: %{pnm_buildrequires_SUNWzlib}
BuildRequires: %{pnm_buildrequires_SUNWcsl}
BuildRequires: %{pnm_buildrequires_SUNWlibms}
BuildRequires: %{pnm_buildrequires_SUNWgss}
BuildRequires: %{pnm_buildrequires_SUNWTcl}
BuildRequires: SFEeditline

Requires: %{pnm_requires_SUNWlxsl}
Requires: %{pnm_requires_SUNWlxml}
Requires: %{pnm_requires_SUNWzlib}
Requires: %{pnm_requires_SUNWcsl}
Requires: %{pnm_requires_SUNWopenssl}
Requires: %{pnm_requires_SUNWlibms}
Requires: %{pnm_requires_SUNWgss}
Requires: SFEeditline

Requires: %{name}-library

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):	 	PostgreSQL Global Development Group
Meta(info.maintainer):	 	pkglabo.justplayer.com <pkgadmin@justplayer.com>
# Meta(info.repository_url):	[open source code repository]
Meta(info.classification):	System Database

%description
PostgreSQL is a powerful, open source object-relational database system. It has more than 15 years of active development and a proven architecture that has earned it a strong reputation for reliability, data integrity, and correctness. It runs on all major operating systems, including Linux, UNIX (AIX, BSD, HP-UX, SGI IRIX, Mac OS X, Solaris, Tru64), and Windows. It is fully ACID compliant, has full support for foreign keys, joins, views, triggers, and stored procedures (in multiple languages). It includes most SQL:2008 data types, including INTEGER, NUMERIC, BOOLEAN, CHAR, VARCHAR, DATE, INTERVAL, and TIMESTAMP. It also supports storage of binary large objects, including pictures, sounds, or video. It has native programming interfaces for C/C++, Java, .Net, Perl, Python, Ruby, Tcl, ODBC, among others, and exceptional documentation. 

%package library

IPS_package_name: database/postgres-91/library
Summary: PostgreSQL client libraries
Requires: %{pnm_requires_SUNWlibms}
Requires: %{pnm_requires_SUNWcsl}

%package languages
IPS_package_name: database/postgres-91/language-bindings
Summary: PostgreSQL additional Perl, Python & TCL server procedural languages

Requires: %pnm_requires_perl_default
Requires: runtime/python-26
Requires: %{pnm_requires_SUNWlibms}
Requires: %{pnm_requires_SUNWcsl}
Requires: %{pnm_requires_SUNWTcl}
Requires: %{name}
Requires: %{name}-library

%package developer
IPS_package_name: database/postgres-91/developer
Summary: PostgreSQL development tools and header files

Requires: %{pnm_requires_SUNWlxsl}
Requires: %{pnm_requires_SUNWlxml}
Requires: %{pnm_requires_SUNWgss}
Requires: %{pnm_requires_SUNWopenssl}
Requires: %{pnm_requires_SUNWcsl}
Requires: %{pnm_requires_SUNWzlib}
Requires: %{pnm_requires_SUNWlibms}
Requires: %{name}
Requires: %{name}-library

%package documentation
IPS_package_name: database/postgres-91/documentation
Summary: PostgreSQL documentation and man pages

%package server
IPS_package_name: service/database/postgres-91
Summary: PostgreSQL database server

%define _basedir         /
SUNW_Basedir:            %{_basedir}

Requires: %{pnm_requires_SUNWlxsl}
Requires: %{pnm_requires_SUNWlxml}
Requires: %{pnm_requires_SUNWgss}
Requires: %{pnm_requires_SUNWopenssl}
Requires: %{pnm_requires_SUNWcsl}
Requires: %{pnm_requires_SUNWzlib}
Requires: %{pnm_requires_SUNWlibms}
Requires: %{name}
Requires: %{name}-library

%package contrib
IPS_package_name: database/postgres-91/contrib
Summary: PostgreSQL community contributed tools not part of core product

Requires: %{pnm_requires_SUNWlxsl}
Requires: %{pnm_requires_SUNWlxml}
Requires: %{pnm_requires_SUNWgss}
Requires: %{pnm_requires_SUNWopenssl}
Requires: %{pnm_requires_SUNWcsl}
Requires: %{pnm_requires_SUNWzlib}
Requires: %{pnm_requires_SUNWlibms}
Requires: %{name}
Requires: %{name}-library

%prep
%setup -c -n %{tarball_name}-%{tarball_version}
#%patch1 -p0

%ifarch amd64 sparcv9
rm -rf %{tarball_name}-%{tarball_version}-64
cp -rp %{tarball_name}-%{tarball_version} %{tarball_name}-%{tarball_version}-64
%endif

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{tarball_name}-%{tarball_version}
%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

export CCAS=/usr/bin/cc
export CCASFLAGS=
export CC=cc
# export CFLAGS="%optflags"
export CFLAGS="-i -xO4 -xspace -xstrconst -Kpic -xregs=no%frameptr -xCC"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -lncurses"
export LD_OPTIONS="-R/usr/sfw/lib:/usr/gnu/lib -L/usr/sfw/lib:/usr/gnu/lib"

./configure --prefix=%{_prefix}/%{major_version} \
            --exec-prefix=%{_prefix}/%{major_version} \
            --bindir=%{_prefix}/%{major_version}/bin \
            --libexecdir=%{_prefix}/%{major_version}/bin \
            --sbindir=%{_prefix}/%{major_version}/bin \
            --datadir=%{_prefix}/%{major_version}/share \
            --sysconfdir=%{_prefix}/%{major_version}/etc \
            --mandir=%{_prefix}/%{major_version}/man \
            --libdir=%{_prefix}/%{major_version}/lib \
            --includedir=%{_prefix}/%{major_version}/include \
            --sharedstatedir=%{_var_prefix}/%{major_version} \
            --localstatedir=%{_var_prefix}/%{major_version} \
            --localedir=%{_prefix}/%{major_version}/share/locale/ \
            --enable-nls \
            --docdir=%{_prefix}/%{major_version}/doc \
            --with-system-tzdata=/usr/share/lib/zoneinfo \
            --with-tcl \
            --with-perl \
            --with-python \
            --with-pam \
            --with-openssl \
            --with-libedit-preferred \
            --with-libxml \
            --with-libxslt \
            --with-gssapi \
            --enable-thread-safety \
            --enable-dtrace \
            --with-includes=/usr/include:/usr/sfw/include:/usr/sfw/include:/usr/gnu/include \
            --with-tclconfig=/usr/lib \
            --with-libs=/usr/lib:/usr/sfw/lib:/usr/gnu/lib

gmake -j$CPUS world

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64

#export CFLAGS="%optflags64"
export CFLAGS="-m64 -i -xO4 -xspace -xstrconst -Kpic -xregs=no%frameptr -xCC"
export LDFLAGS="%_ldflags -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -lncurses"
export LD_OPTIONS="-R/usr/sfw/lib/%{_arch64}:/usr/gnu/lib/%{_arch64} -L/usr/sfw/lib/%{_arch64}:/usr/gnu/lib/%{_arch64}"

./configure --prefix=%{_prefix}/%{major_version} \
            --exec-prefix=%{_prefix}/%{major_version} \
            --bindir=%{_prefix}/%{major_version}/bin/%{_arch64} \
            --libexecdir=%{_prefix}/%{major_version}/bin/%{_arch64} \
            --sbindir=%{_prefix}/%{major_version}/bin/%{_arch64} \
            --datadir=%{_prefix}/%{major_version}/share \
            --sysconfdir=%{_prefix}/%{major_version}/etc \
            --mandir=%{_prefix}/%{major_version}/man \
            --libdir=%{_prefix}/%{major_version}/lib/%{_arch64} \
            --includedir=%{_prefix}/%{major_version}/include \
            --sharedstatedir=%{_var_prefix}/%{major_version} \
            --localstatedir=%{_var_prefix}/%{major_version} \
            --localedir=%{_prefix}/%{major_version}/share/locale/ \
            --enable-nls \
            --docdir=%{_prefix}/%{major_version}/doc \
            --with-system-tzdata=/usr/share/lib/zoneinfo \
            --with-tcl \
            --with-python \
            --with-pam \
            --with-openssl \
            --with-libedit-preferred \
            --with-libxml \
            --with-libxslt \
            --with-gssapi \
            --enable-thread-safety \
            --enable-dtrace \
            --with-includes=/usr/include:/usr/sfw/include:/usr/sfw/include:/usr/gnu/include \
            --with-tclconfig=/usr/lib \
            --with-libs=/usr/lib/%{_arch64}:/usr/sfw/lib/%{_arch64}:/usr/gnu/lib/%{_arch64}

gmake -j$CPUS world

%endif
%install
cd %{tarball_name}-%{tarball_version}
gmake install-world DESTDIR=$RPM_BUILD_ROOT
if test -d sun-manpages; then
	cd sun-manpages
	make install DESTDIR=$RPM_BUILD_ROOT
	cd ..
fi

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64
gmake install-world DESTDIR=$RPM_BUILD_ROOT

#export OLD_PATH=`pwd`
#cd $RPM_BUILD_ROOT%{_prefix}/%{major_version}/bin
#ln -s %{_arch64} 64
#cd ../lib
#ln -s %{_arch64} 64
#cd ${OLD_PATH}
#cd ..
%endif

mkdir -p $RPM_BUILD_ROOT/etc/security
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/%{major_version}/backups
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/%{major_version}/data
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/%{major_version}/data_64

mkdir -p $RPM_BUILD_ROOT/lib/svc/method/
cp %{SOURCE1} $RPM_BUILD_ROOT/lib/svc/method/postgres_91
chmod +x $RPM_BUILD_ROOT/lib/svc/method/postgres_91
mkdir -p $RPM_BUILD_ROOT/var/svc/manifest/application/database/
cp %{SOURCE2} $RPM_BUILD_ROOT/var/svc/manifest/application/database/postgresql_91.xml

# attribute
mkdir -p $RPM_BUILD_ROOT/etc/security/auth_attr.d/
cp %{SOURCE3} $RPM_BUILD_ROOT/etc/security/auth_attr.d/service\%2Fdatabase\%2Fpostgres-91
mkdir -p $RPM_BUILD_ROOT/etc/security/exec_attr.d/
cp %{SOURCE4} $RPM_BUILD_ROOT/etc/security/exec_attr.d/service\%2Fdatabase\%2Fpostgres-91
mkdir -p $RPM_BUILD_ROOT/etc/security/prof_attr.d/
cp %{SOURCE5} $RPM_BUILD_ROOT/etc/security/prof_attr.d/service\%2Fdatabase\%2Fpostgres-91
mkdir -p $RPM_BUILD_ROOT/etc/user_attr.d/
cp %{SOURCE5} $RPM_BUILD_ROOT/etc/user_attr.d/service\%2Fdatabase\%2Fpostgres-91


mkdir -p $RPM_BUILD_ROOT/usr/share

# delete amd64
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libecpg.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libpq.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libpgtypes.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/amd64
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libpgport.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libecpg_compat.a

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

# make symbolic link

cd $RPM_BUILD_ROOT/%{_prefix}/%{major_version}/bin/
[ -r 64 ] || ln -s amd64 64

# plpython is out in postgresql 9.1
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/plpython-%{major_version}.mo

%clean
rm -rf $RPM_BUILD_ROOT

%actions server
group groupname="postgres"
user ftpuser=false gcos-field="PostgreSQL Reserved UID" username="postgres" password=NP group="postgres"

%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/amd64
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
# %{_prefix}/%{major_version}/bin/64
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/clusterdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/createdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/createlang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/createuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/dropdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/droplang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/dropuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_basebackup
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_dump
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_dumpall
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_restore
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_test_fsync
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/vacuumdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/reindexdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/psql
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/psql
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/clusterdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/createdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/createlang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/createuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/dropdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/droplang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/dropuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_basebackup
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_dump
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_dumpall
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_restore
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_test_fsync
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/reindexdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/vacuumdb
%attr (0644, root, other) %{_prefix}/%{major_version}/share/psqlrc.sample
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_basebackup-%{major_version}.mo


%files library
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%attr (0755, root, bin) %{_prefix}/%{major_version}/bin/64
#%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man/man5
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpgport.a
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpq.a
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libecpg.a
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.a
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.a
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/auth_delay.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/dummy_seclabel.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/file_fdw.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg.so.6
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg.so.6.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpq.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpq.so.5.4
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpgtypes.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg_compat.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg_compat.so.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg_compat.so.3.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpgtypes.so.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpgtypes.so.3.2
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpq.so.5
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/auth_delay.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/dummy_seclabel.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/file_fdw.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg.so.6
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg.so.6.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.so.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.so.3.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.so.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.so.3.2
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpq.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpq.so.5
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpq.so.5.4
 
%files languages
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/extension
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pltcl_listmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pltcl_loadmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pltcl_delmod
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/plperl-%{major_version}.mo
#%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pltcl-%{major_version}.mo
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/plpython.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/pltcl.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plperl.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plpython.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/pltcl.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pltcl_delmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pltcl_listmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pltcl_loadmod
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/unknown.pltcl
%{_prefix}/%{major_version}/share/extension/plperl--1.0.sql
%{_prefix}/%{major_version}/share/extension/plperl--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/plperl.control
%{_prefix}/%{major_version}/share/extension/plperlu--1.0.sql
%{_prefix}/%{major_version}/share/extension/plperlu--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/plperlu.control
%{_prefix}/%{major_version}/share/extension/plpython2u--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpython2u--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpython2u.control
%{_prefix}/%{major_version}/share/extension/plpython3u--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpython3u--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpython3u.control
%{_prefix}/%{major_version}/share/extension/plpythonu--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpythonu--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/plpythonu.control
%{_prefix}/%{major_version}/share/extension/pltcl--1.0.sql
%{_prefix}/%{major_version}/share/extension/pltcl--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pltcl.control
%{_prefix}/%{major_version}/share/extension/pltclu--1.0.sql
%{_prefix}/%{major_version}/share/extension/pltclu--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pltclu.control


%files developer
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/config
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/makefiles
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/test
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/test/regress
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/config
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/makefiles
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/test
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/test/regress
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/config/install-sh
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/Makefile.port
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/Makefile.shlib
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/makefiles/pgxs.mk
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/nls-global.mk
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/ecpg
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_config
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/ecpg
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_config
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/config/install-sh
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/Makefile.global
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/Makefile.port
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/Makefile.shlib
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/makefiles/pgxs.mk
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/nls-global.mk
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/test/regress/pg_regress
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/Makefile.global
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/test/regress/pg_regress
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/*

%files documentation
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/doc
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/doc/html
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man
%{_prefix}/%{major_version}/doc/html/*
%{_prefix}/%{major_version}/man/*
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/doc/extension
%{_prefix}/%{major_version}/doc/extension/*

%files server
%defattr (-, root, bin)

%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/extension
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share/timezonesets
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share/tsearch_data
%dir %attr (0755, postgres, postgres) %{_var_prefix}
%dir %attr (0755, postgres, postgres) %{_var_prefix}/%{major_version}
%dir %attr (0700, postgres, postgres) %{_var_prefix}/%{major_version}/backups
%dir %attr (0700, postgres, postgres) %{_var_prefix}/%{major_version}/data
%dir %attr (0700, postgres, postgres) %{_var_prefix}/%{major_version}/data_64
%dir %attr (0755, root, sys) /etc
%dir %attr (0755, root, sys) /etc/security
%dir %attr (0755, root, sys) /etc/security/auth_attr.d
%dir %attr (0755, root, sys) /etc/security/exec_attr.d
%dir %attr (0755, root, sys) /etc/security/prof_attr.d
%dir %attr (0755, root, sys) /etc/user_attr.d
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) /var/svc
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/application
%dir %attr (0755, root, sys) /var/svc/manifest/application/database
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hungarian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hunspell_sample.affix
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/ispell_sample.affix
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/ispell_sample.dict
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/italian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/norwegian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/portuguese.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/russian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/spanish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/swedish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/synonym_sample.syn
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/thesaurus_sample.ths
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/turkish.stop
%attr (0555, root, bin) /lib/svc/method/postgres_91
%attr (0644, root, sys) /etc/security/auth_attr.d/service\%2Fdatabase\%2Fpostgres-91
%attr (0644, root, sys) /etc/security/exec_attr.d/service\%2Fdatabase\%2Fpostgres-91
%attr (0644, root, sys) /etc/security/prof_attr.d/service\%2Fdatabase\%2Fpostgres-91
%attr (0644, root, sys) /etc/user_attr.d/service\%2Fdatabase\%2Fpostgres-91
%attr (0444, root, sys) /var/svc/manifest/application/database/postgresql_91.xml
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/initdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_controldata
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_ctl
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_resetxlog
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/postgres
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/initdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_controldata
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_ctl
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_resetxlog
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/postgres
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/postmaster
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/postmaster
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/ascii_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/cyrillic_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/dict_snowball.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_cn_and_mic.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_jis_2004_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_jp_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_kr_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_tw_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/latin2_and_win1250.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/latin_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/plpgsql.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_ascii.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_cyrillic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_cn.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_jp.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_kr.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_tw.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_gb18030.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_gbk.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_iso8859.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_iso8859_1.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_johab.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_uhc.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_win.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/ascii_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/cyrillic_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/dict_snowball.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_cn_and_mic.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_jis_2004_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_jp_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_kr_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_tw_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/latin2_and_win1250.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/latin_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plpgsql.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_ascii.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_cyrillic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_cn.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_jp.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_kr.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_tw.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_gb18030.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_gbk.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_iso8859.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_iso8859_1.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_johab.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_uhc.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_win.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc2004_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpqwalreceiver.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plpython2.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc2004_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/plpython2.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpqwalreceiver.so
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/*/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/conversion_create.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/information_schema.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/pg_hba.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/pg_ident.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/pg_service.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgres.bki
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgres.description
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgres.shdescription
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgresql.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/recovery.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/snowball_create.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/sql_features.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/system_views.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Africa.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/America.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Antarctica.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Asia.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Atlantic.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Australia
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Australia.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Default
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Etc.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Europe.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/India
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Indian.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Pacific.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/danish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/dutch.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/english.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/finnish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/french.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/german.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/extension/plpgsql--1.0.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/extension/plpgsql--unpackaged--1.0.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/extension/plpgsql.control

%files contrib
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/extension
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share/tsearch_data
%{_prefix}/%{major_version}/lib/adminpack.so
%{_prefix}/%{major_version}/lib/auto_explain.so
%{_prefix}/%{major_version}/lib/btree_gin.so
%{_prefix}/%{major_version}/lib/btree_gist.so
%{_prefix}/%{major_version}/lib/chkpass.so
%{_prefix}/%{major_version}/lib/citext.so
%{_prefix}/%{major_version}/lib/cube.so
%{_prefix}/%{major_version}/lib/dblink.so
%{_prefix}/%{major_version}/lib/dict_int.so
%{_prefix}/%{major_version}/lib/dict_xsyn.so
%{_prefix}/%{major_version}/lib/earthdistance.so
%{_prefix}/%{major_version}/lib/fuzzystrmatch.so
%{_prefix}/%{major_version}/lib/hstore.so
%{_prefix}/%{major_version}/lib/_int.so
%{_prefix}/%{major_version}/lib/isn.so
%{_prefix}/%{major_version}/lib/lo.so
%{_prefix}/%{major_version}/lib/ltree.so
%{_prefix}/%{major_version}/lib/pageinspect.so
%{_prefix}/%{major_version}/lib/passwordcheck.so
%{_prefix}/%{major_version}/lib/pg_buffercache.so
%{_prefix}/%{major_version}/lib/pg_freespacemap.so
%{_prefix}/%{major_version}/lib/pg_stat_statements.so
%{_prefix}/%{major_version}/lib/pg_trgm.so
%{_prefix}/%{major_version}/lib/pg_upgrade_support.so
%{_prefix}/%{major_version}/lib/pgcrypto.so
%{_prefix}/%{major_version}/lib/pgrowlocks.so
%{_prefix}/%{major_version}/lib/pgstattuple.so
%{_prefix}/%{major_version}/lib/seg.so
%{_prefix}/%{major_version}/lib/autoinc.so
%{_prefix}/%{major_version}/lib/insert_username.so
%{_prefix}/%{major_version}/lib/moddatetime.so
%{_prefix}/%{major_version}/lib/refint.so
%{_prefix}/%{major_version}/lib/timetravel.so
%{_prefix}/%{major_version}/lib/tablefunc.so
%{_prefix}/%{major_version}/lib/test_parser.so
%{_prefix}/%{major_version}/lib/tsearch2.so
%{_prefix}/%{major_version}/lib/unaccent.so
%{_prefix}/%{major_version}/lib/sslinfo.so
%{_prefix}/%{major_version}/lib/pgxml.so
%{_prefix}/%{major_version}/lib/amd64/autoinc.so
%{_prefix}/%{major_version}/lib/amd64/adminpack.so
%{_prefix}/%{major_version}/lib/amd64/auto_explain.so
%{_prefix}/%{major_version}/lib/amd64/btree_gin.so
%{_prefix}/%{major_version}/lib/amd64/btree_gist.so
%{_prefix}/%{major_version}/lib/amd64/chkpass.so
%{_prefix}/%{major_version}/lib/amd64/citext.so
%{_prefix}/%{major_version}/lib/amd64/cube.so
%{_prefix}/%{major_version}/lib/amd64/dblink.so
%{_prefix}/%{major_version}/lib/amd64/dict_int.so
%{_prefix}/%{major_version}/lib/amd64/dict_xsyn.so
%{_prefix}/%{major_version}/lib/amd64/earthdistance.so
%{_prefix}/%{major_version}/lib/amd64/fuzzystrmatch.so
%{_prefix}/%{major_version}/lib/amd64/hstore.so
%{_prefix}/%{major_version}/lib/amd64/_int.so
%{_prefix}/%{major_version}/lib/amd64/insert_username.so
%{_prefix}/%{major_version}/lib/amd64/isn.so
%{_prefix}/%{major_version}/lib/amd64/lo.so
%{_prefix}/%{major_version}/lib/amd64/ltree.so
%{_prefix}/%{major_version}/lib/amd64/moddatetime.so
%{_prefix}/%{major_version}/lib/amd64/pageinspect.so
%{_prefix}/%{major_version}/lib/amd64/passwordcheck.so
%{_prefix}/%{major_version}/lib/amd64/pg_buffercache.so
%{_prefix}/%{major_version}/lib/amd64/pg_freespacemap.so
%{_prefix}/%{major_version}/lib/amd64/pg_stat_statements.so
%{_prefix}/%{major_version}/lib/amd64/pg_trgm.so
%{_prefix}/%{major_version}/lib/amd64/pg_upgrade_support.so
%{_prefix}/%{major_version}/lib/amd64/pgcrypto.so
%{_prefix}/%{major_version}/lib/amd64/pgrowlocks.so
%{_prefix}/%{major_version}/lib/amd64/pgstattuple.so
%{_prefix}/%{major_version}/lib/amd64/pgxml.so
%{_prefix}/%{major_version}/lib/amd64/refint.so
%{_prefix}/%{major_version}/lib/amd64/seg.so
%{_prefix}/%{major_version}/lib/amd64/sslinfo.so
%{_prefix}/%{major_version}/lib/amd64/tablefunc.so
%{_prefix}/%{major_version}/lib/amd64/test_parser.so
%{_prefix}/%{major_version}/lib/amd64/timetravel.so
%{_prefix}/%{major_version}/lib/amd64/tsearch2.so
%{_prefix}/%{major_version}/lib/amd64/unaccent.so
%{_prefix}/%{major_version}/share/extension/adminpack--1.0.sql
%{_prefix}/%{major_version}/share/extension/adminpack.control
%{_prefix}/%{major_version}/share/extension/autoinc--1.0.sql
%{_prefix}/%{major_version}/share/extension/autoinc--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/autoinc.control
%{_prefix}/%{major_version}/share/extension/btree_gin--1.0.sql
%{_prefix}/%{major_version}/share/extension/btree_gin--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/btree_gin.control
%{_prefix}/%{major_version}/share/extension/btree_gist--1.0.sql
%{_prefix}/%{major_version}/share/extension/btree_gist--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/btree_gist.control
%{_prefix}/%{major_version}/share/extension/chkpass--1.0.sql
%{_prefix}/%{major_version}/share/extension/chkpass--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/chkpass.control
%{_prefix}/%{major_version}/share/extension/citext--1.0.sql
%{_prefix}/%{major_version}/share/extension/citext--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/citext.control
%{_prefix}/%{major_version}/share/extension/cube--1.0.sql
%{_prefix}/%{major_version}/share/extension/cube--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/cube.control
%{_prefix}/%{major_version}/share/extension/dblink--1.0.sql
%{_prefix}/%{major_version}/share/extension/dblink--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/dblink.control
%{_prefix}/%{major_version}/share/extension/dict_int--1.0.sql
%{_prefix}/%{major_version}/share/extension/dict_int--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/dict_int.control
%{_prefix}/%{major_version}/share/extension/dict_xsyn--1.0.sql
%{_prefix}/%{major_version}/share/extension/dict_xsyn--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/dict_xsyn.control
%{_prefix}/%{major_version}/share/extension/earthdistance--1.0.sql
%{_prefix}/%{major_version}/share/extension/earthdistance--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/earthdistance.control
%{_prefix}/%{major_version}/share/extension/file_fdw--1.0.sql
%{_prefix}/%{major_version}/share/extension/file_fdw.control
%{_prefix}/%{major_version}/share/extension/fuzzystrmatch--1.0.sql
%{_prefix}/%{major_version}/share/extension/fuzzystrmatch--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/fuzzystrmatch.control
%{_prefix}/%{major_version}/share/extension/hstore--1.0.sql
%{_prefix}/%{major_version}/share/extension/hstore--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/hstore.control
%{_prefix}/%{major_version}/share/extension/insert_username--1.0.sql
%{_prefix}/%{major_version}/share/extension/insert_username--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/insert_username.control
%{_prefix}/%{major_version}/share/extension/intagg--1.0.sql
%{_prefix}/%{major_version}/share/extension/intagg--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/intagg.control
%{_prefix}/%{major_version}/share/extension/intarray--1.0.sql
%{_prefix}/%{major_version}/share/extension/intarray--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/intarray.control
%{_prefix}/%{major_version}/share/extension/isn--1.0.sql
%{_prefix}/%{major_version}/share/extension/isn--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/isn.control
%{_prefix}/%{major_version}/share/extension/lo--1.0.sql
%{_prefix}/%{major_version}/share/extension/lo--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/lo.control
%{_prefix}/%{major_version}/share/extension/ltree--1.0.sql
%{_prefix}/%{major_version}/share/extension/ltree--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/ltree.control
%{_prefix}/%{major_version}/share/extension/moddatetime--1.0.sql
%{_prefix}/%{major_version}/share/extension/moddatetime--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/moddatetime.control
%{_prefix}/%{major_version}/share/extension/pageinspect--1.0.sql
%{_prefix}/%{major_version}/share/extension/pageinspect--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pageinspect.control
%{_prefix}/%{major_version}/share/extension/pg_buffercache--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_buffercache--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_buffercache.control
%{_prefix}/%{major_version}/share/extension/pg_freespacemap--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_freespacemap--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_freespacemap.control
%{_prefix}/%{major_version}/share/extension/pg_stat_statements--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_stat_statements--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_stat_statements.control
%{_prefix}/%{major_version}/share/extension/pg_trgm--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_trgm--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pg_trgm.control
%{_prefix}/%{major_version}/share/extension/pgcrypto--1.0.sql
%{_prefix}/%{major_version}/share/extension/pgcrypto--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pgcrypto.control
%{_prefix}/%{major_version}/share/extension/pgrowlocks--1.0.sql
%{_prefix}/%{major_version}/share/extension/pgrowlocks--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pgrowlocks.control
%{_prefix}/%{major_version}/share/extension/pgstattuple--1.0.sql
%{_prefix}/%{major_version}/share/extension/pgstattuple--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/pgstattuple.control
%{_prefix}/%{major_version}/share/extension/refint--1.0.sql
%{_prefix}/%{major_version}/share/extension/refint--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/refint.control
%{_prefix}/%{major_version}/share/extension/seg--1.0.sql
%{_prefix}/%{major_version}/share/extension/seg--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/seg.control
%{_prefix}/%{major_version}/share/extension/sslinfo--1.0.sql
%{_prefix}/%{major_version}/share/extension/sslinfo--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/sslinfo.control
%{_prefix}/%{major_version}/share/extension/tablefunc--1.0.sql
%{_prefix}/%{major_version}/share/extension/tablefunc--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/tablefunc.control
%{_prefix}/%{major_version}/share/extension/test_parser--1.0.sql
%{_prefix}/%{major_version}/share/extension/test_parser--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/test_parser.control
%{_prefix}/%{major_version}/share/extension/timetravel--1.0.sql
%{_prefix}/%{major_version}/share/extension/timetravel--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/timetravel.control
%{_prefix}/%{major_version}/share/extension/tsearch2--1.0.sql
%{_prefix}/%{major_version}/share/extension/tsearch2--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/tsearch2.control
%{_prefix}/%{major_version}/share/extension/unaccent--1.0.sql
%{_prefix}/%{major_version}/share/extension/unaccent--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/unaccent.control
%{_prefix}/%{major_version}/share/extension/xml2--1.0.sql
%{_prefix}/%{major_version}/share/extension/xml2--unpackaged--1.0.sql
%{_prefix}/%{major_version}/share/extension/xml2.control
%{_prefix}/%{major_version}/share/tsearch_data/xsyn_sample.rules
%{_prefix}/%{major_version}/share/tsearch_data/unaccent.rules
%{_prefix}/%{major_version}/bin/oid2name
%{_prefix}/%{major_version}/bin/pg_archivecleanup
%{_prefix}/%{major_version}/bin/pg_standby
%{_prefix}/%{major_version}/bin/pg_upgrade
%{_prefix}/%{major_version}/bin/pgbench
%{_prefix}/%{major_version}/bin/vacuumlo
%{_prefix}/%{major_version}/bin/amd64/oid2name
%{_prefix}/%{major_version}/bin/amd64/pg_archivecleanup
%{_prefix}/%{major_version}/bin/amd64/pg_standby
%{_prefix}/%{major_version}/bin/amd64/pg_upgrade
%{_prefix}/%{major_version}/bin/amd64/pgbench
%{_prefix}/%{major_version}/bin/amd64/vacuumlo

%changelog
* Fri Sep 16 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Bump to 9.1.0
* Sun Jul 31 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- omit -fast option.
* Sun Jun  5 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- fix dependency using for pnm.
* Mon Apr 18 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Bump to 9.0.4
* Fri Feb  4 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Support 9.0.3
* Tue Feb  1 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Fix some problems.
* Tue Jan 25 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Initial Revision
