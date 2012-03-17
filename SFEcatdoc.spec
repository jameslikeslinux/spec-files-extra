#
# spec file for package SFEcatdoc
#
# includes module(s): catdoc
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname catdoc

Name:                    SFEcatdoc
IPS_Package_Name:	 text/catdoc
Summary:                 catdoc and xls2csv - free MS-Office format readers
Group:                   Utility
Version:                 0.94.2
URL:		         http://www.wagner.pp.ru
Source:		         http://ftp.wagner.pp.ru/pub/catdoc/catdoc-%{version}.tar.gz
License: 		 GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
catdoc is program which reads one or more Microsoft word files and
outputs text, contained insinde them to standard output. Therefore it
does same work for .doc files, as unix cat command for plain ASCII
files.

It is now accompanied by xls2csv - program which converts Excel
spreadsheet into comma-separated value file, and catppt - utility to
extract textual information from Powerpoint files

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --disable-wordview                  \
            --with-install-root=$RPM_BUILD_ROOT

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT/usr/share

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_datadir}/catdoc
%{_datadir}/catdoc/*
%{_mandir}/man1/*

%changelog
* Fri Mar 16 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
