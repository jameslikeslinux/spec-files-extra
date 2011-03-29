#
# spec file for package eb
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%include base.inc

%define _prefix /usr
#%define tarball_version  4.4.3
%define tarball_version  4.4.1
%define tarball_name	 eb

Name:                    SFEeblib
IPS_package_name:        library/eb
Summary:                 the library for accessing to the EPWING format Dictionaries
#Version:                 4.4.3
Version:                 4.4.1
License:		 Modified BSDL
Url:                     http://www.sra.co.jp/people/m-kasahr/eb/
Source:                  ftp://ftp.sra.co.jp/pub/misc/%{tarball_name}/%{tarball_name}-%{tarball_version}.tar.bz2
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:		 /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{tarball_name}-%{version}-build

BuildRequires: %{pnm_buildrequires_SUNWbtool}
BuildRequires: %{pnm_buildrequires_SUNWbinutils}
BuildRequires: %{pnm_buildrequires_SUNWzlib}
BuildRequires: %{pnm_buildrequires_SUNWgnu_gettext}
BuildRequires: %{pnm_buildrequires_SUNWxcu4}
BuildRequires: %{pnm_buildrequires_SUNWgmake}

Requires: %{pnm_requires_SUNWzlib}
Requires: %{pnm_requires_SUNWgnu_gettext}

# OpenSolaris IPS Package Manifest Fields
Meta(info.maintainer):	 	pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):	 	Motoyuki Kasahara <m-kasahr@sra.co.jp>
# Meta(info.repository_url):	[open source code repository]
Meta(info.classification):	System Libraries

%description
EB library is for accessing to the EPWING format Dictionaries

#%include default-depend.inc

%prep
%setup -c -n %name-%version
%ifarch amd64 sparcv9
rm -rf %{tarball_name}-%{tarball_version}-64
cp -rp %{tarball_name}-%{tarball_version} %{tarball_name}-%{tarball_version}-64
%endif

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
#export CFLAGS="$RPM_OPT_FLAGS"
#export LDFLAGS="%_ldflags"

cd %{tarball_name}-%{tarball_version}
%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

./configure \
 --prefix=%{_prefix}\
 --sysconfdir=%{_sysconfdir} \
 --libdir=%{_libdir} \
 --bindir=%{_bindir} \
 --includedir=%{_includedir} \
 --mandir=%{_mandir}
gmake -j$CPUS

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64

export CC=gcc
export CXX=g++
export CFLAGS="-O3 -march=opteron -m64 -Xlinker -i -fno-omit-frame-pointer -fPIC -DPIC"
export LDFLAGS="-L/usr/lib/amd64 -R/usr/lib/amd64  -Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect"
#pkgbuild: + export 'CFLAGS=-O3 -march=i586 -Xlinker -i -fno-omit-frame-pointer -fPIC -DPIC'

./configure \
 --prefix=%{_prefix}\
 --sysconfdir=%{_sysconfdir} \
 --libdir=%{_libdir}/%{_arch64} \
 --bindir=%{_bindir}/%{_arch64} \
 --includedir=%{_includedir} \
 --mandir=%{_mandir}
gmake -j$CPUS

%endif

%install
cd %{tarball_name}-%{tarball_version}
gmake install DESTDIR=$RPM_BUILD_ROOT
if test -d sun-manpages; then
	cd sun-manpages
	make install DESTDIR=$RPM_BUILD_ROOT
	cd ..
fi

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64
gmake install DESTDIR=$RPM_BUILD_ROOT

cd ..
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{tarball_name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, bin) %{_prefix}/include/eb
%{_prefix}/include/eb/*
%dir %attr(0755, root, sys) %{_prefix}
%dir %attr(0755, root, sys) %{_prefix}/share
%attr(0755, root, other) %{_prefix}/share/*
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/eb.conf

%changelog
* Wed May  6 2009 TAKI, Yasushi <taki@justplayer.com>
- Initial Revision
* Mon Mar  8 2010 TAKI, Yasushi <taki@justplayer.com>
- delete sub packages
- support source juicer
* Tue Mar 29 2011 TAKI, Yasushi <taki@justplayer.com>
- change for sfe.
- support package name macros.
- change strict permission
* Tue Mar 29 2011 TAKI, Yasushi <taki@justplayer.com>
- version down 4.4.3 to 4.4.1, because 4.4.3 does not work correctly.
