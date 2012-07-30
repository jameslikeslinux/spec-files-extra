#
# spec file for package zsnes
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:         zsnes
License:      GPL
Version:      1.51
%define fileversion %( echo %version | perl -pe "s/\.//" )
%define buildversion %( echo %version | perl -pe "s/\./_/" )
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      ZSNES - Super Nintendo emulator
Source:       http://prdownloads.sourceforge.net/zsnes/zsnes%{fileversion}src.tar.bz2
URL:          http://www.zsnes.com/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n %name\_%buildversion


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd src
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --sysconfdir=%{_sysconfdir}

gmake -j$CPUS 

%install
cd src
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Dec 16 2011 - James Choi
- initial spec
