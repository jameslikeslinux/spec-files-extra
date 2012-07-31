
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#

%define major_minor      2.2

Name:                    libsigc++
License:                 LGPL
Group:                   System/Libraries
Version:                 2.2.10
Release:                 1
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 Libsigc++ - a library that implements a typesafe callback system for standard C++
URL:                     http://libsigc.sourceforge.net
Source:                  http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%major_minor/%{name}-%{version}.tar.bz2
#Patch1:                  sigcpp-01-build-fix.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n libsigc++-%version
#%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
perl -pi -e 's/(\s*#define SIGC_TYPEDEF_REDEFINE_ALLOWED.*)/\/\/$1/' \
    sigc++/macros/signal.h.m4
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT%{_datadir}/doc
mv libsigc++-2.0 libsigc++-2.2
popd


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Aug  5 2011 - Alex Viskovatoff
- Bump to 2.2.10
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.2.2.
* Fri Feb 29 2008 - elaine.xiong@sun.com
- Bump to 2.2.1 that resolves build failure of 2.0 with CC.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.0.
* Fri Feb 22 2008 - elaine.xiong@sun.com
- Include tests binaries into dev package.
* Tue Feb 12 2008 - ghee.teo@sun.com
- Clean up %files section
* Fri Feb 01 2008 - elaine.xiong@sun.com
- create. split from SFEsigcpp.spec
