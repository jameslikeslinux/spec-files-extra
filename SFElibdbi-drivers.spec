
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define src_version 0.8.3-1
#just in case, use for 0.8.3-1 -> 0.8.3.1
%define ips_version 0.8.3.1

%define src_name libdbi-drivers

Name:		SFElibdbi-drivers
IPS_Package_Name:	library/dbi-drivers
Summary:	database-independent abstraction layer - Database drivers (libdbi-drivers)
Version:	%{src_version}
IPS_component_version: %{ips_version}
URL:		http://libdbi-drivers.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Group:		System/Libraries
License:	LGPL
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
SUNW_Copyright: %{name}.copyright

%include default-depend.inc

BuildRequires:  SFElibdbi-devel
Requires:       SFElibdbi

#BuildRequires:  mysql
#BuildRequires:  sqlite3
#BuildRequires:  postgresql
#verlagern in subpakete!
#Requires:       SFElibdbi

#%package devel
#Summary:	%{summary} - development files
#SUNW_BaseDir:	%{_basedir}
#%include default-depend.inc
#Requires: %name

%description
The libdbi-drivers project provides the database-specific drivers for the libdbi framework.
libdbi implements a database-independent abstraction layer in C, similar to the DBI/DBD layer in Perl. Writing one generic set of code, programmers can leverage the power of multiple databases and multiple simultaneous database connections by using this framework.

The drivers officially supported by libdbi are:

    Firebird/Interbase
    FreeTDS (provides access to MS SQL Server and Sybase)
    MySQL
    PostgreSQL
    SQLite/SQLite3

For other drivers see the web page of the project.

%prep
%setup -q -n %{src_name}-%{version}

%build

export CFLAGS="%optflags -L%{_prefix}/%{mysql_default_libdir}/mysql -R%{_prefix}/%{mysql_default_libdir}/mysql"
export LDFLAGS="%{_ldflags} -L%{_prefix}/%{mysql_default_libdir}/mysql -R%{_prefix}/%{mysql_default_libdir}/mysql"

./configure --prefix=%{_prefix} --disable-static  \
            --with-mysql            \
            --with-mysql-incdir=%{_prefix}/%{mysql_default_includedir} \
            --with-mysql-libdir=%{_prefix}/%{mysql_default_libdir}/mysql \
            --with-pgsql            \
            --with-pgsql-dir=/usr/postgres/8.4 \
            --with-pgsql-incdir=/usr/postgres/8.4/include \
            --with-pgsql-libdir=/usr/postgres/8.4/lib \

            #--with-sqlite3          \
            #--with-sqlite3-dir      \
            #--with-sqlite3-incdir   \
            #--with-sqlite3-libdir   \
            #--with-msql             \
            #--with-msql-dir         \
            #--with-msql-incdir      \
            #--with-msql-libdir      \
  
gmake

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

#%files devel
#%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_includedir}
#%{_includedir}/*

%dir %attr (0755, root, sys) %{_datadir} 
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*


%changelog
* Sat Aug 11 2012 - Thomas Wagner
- initial spec
