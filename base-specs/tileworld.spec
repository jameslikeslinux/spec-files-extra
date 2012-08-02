#
# spec file for package tileworld
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:         tileworld
License:      MIT
Version:      1.3.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Tileworld - Chip's Challenge
Source:       http://www.muppetlabs.com/~breadbox/pub/software/tworld/tworld-%{version}.tar.gz

URL:          http://www.muppetlabs.com/~breadbox/software/tworld
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n tworld-%version


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir}

cp Makefile Makefile.old

gmake -j$CPUS 

%install
perl -pi -e "s|prefix = \/usr|prefix = $RPM_BUILD_ROOT\/usr|" Makefile
perl -pi -e "s|mandir = \/usr\/share\/man|mandir = $RPM_BUILD_ROOT\/usr\/share\/man|" Makefile
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Dec 16 2011 - jchoi42@pha.jhu.edu
- initial spec
