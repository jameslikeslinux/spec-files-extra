#
# spec file for package qhull
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:         qhull
License:      BSD
Group:        System/Libraries
Version:      2011.2
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Implements the Quickhull algorithm
Source:       http://www.qhull.org/download/qhull-%{version}-src.tgz
URL:          http://www.qhull.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n qhull-%version


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

gmake -j$CPUS 


%install
#gmake install DESTDIR=$RPM_BUILD_ROOT$prefixdir
gmake install DESTDIR=$RPM_BUILD_ROOT/usr


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Jan 13 2012 - James Choi
- Initial spec
