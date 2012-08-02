#
# spec file for package SFEpigz
#
# includes module(s): pigz
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname pigz

Name:                    SFEpigz
IPS_Package_Name:	 compress/pigz
Summary:                 pigz - A parallel implementation of gzip
Group:                   Utility
Version:                 2.2.4
URL:		         http://zlib.net/pigz/
Source:		         http://zlib.net/pigz/pigz-%{version}.tar.gz
License: 		 ZLib License
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWzlib
Requires: SUNWzlib

%description
pigz, which stands for parallel implementation of gzip, is a fully
functional replacement for gzip that exploits multiple processors and
multiple cores to the hilt when compressing data. pigz was written by
Mark Adler, and uses the zlib and pthread libraries.

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
make CC="$CC" CFLAGS="$CFLAGS" -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mv pigz unpigz $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mv pigz.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Wed July 4 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
