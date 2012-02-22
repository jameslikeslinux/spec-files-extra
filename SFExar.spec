#
# spec file for package SFExar
#
# includes module(s): xar
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname xar

Name:                    SFExar
IPS_Package_Name:	 compress/xar
Summary:                 XAR - eXtensible ARchiver
Group:                   Utility
Version:                 1.5.2
URL:		         http://code.google.com/p/%srcname/
Source:		         http://%srcname.googlecode.com/files/%srcname-%version.tar.gz
License: 		 New BSD License
Patch1:                  xar-01-configure.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: library/libxml2

%description
The XAR project aims to provide an easily extensible archive
format. Important design decisions include an easily extensible XML
table of contents for random access to archived files, storing the toc
at the beginning of the archive to allow for efficient handling of
streamed archives, the ability to handle files of arbitrarily large
sizes, the ability to choose independent encodings for individual
files in the archive, the ability to store checksums for individual
files in both compressed and uncompressed form, and the ability to
query the table of content''s rich meta-data.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
# Please note system provided libast as referenced below is not the
# same as SFE provided libast. Also note that this is AT&T's
# libast. It is not present on Solaris 10. If you want to port this
# package to Solaris 10 you might consider adding a spec file for
# AT&T's libast on Solaris 10.
export LDFLAGS="%_ldflags /usr/lib/libast.so.1"
export CPPFLAGS="-I/usr/include -I/usr/include/ast"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_includedir}
%dir %attr(0755, root, sys) %{_includedir}/xar
%{_includedir}/xar/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libxar.*

%changelog
* Sun Feb 21 2012- logan@gedanken.org
- Initial spec.
