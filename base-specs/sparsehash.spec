#
# spec file for package sparsehash
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:         sparsehash
License:      BSD
Group:        System/Libraries
Version:      1.12
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      An extremely memory-efficient hash_map implementation
Source:       http://google-sparsehash.googlecode.com/files/sparsehash-%{version}.tar.gz
URL:          http://code.google.com/p/google-sparsehash/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n sparsehash-%version


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*


%changelog
* Fri Jan 13 2012 - James Choi
- Initial spec
