#
# spec libedit for package file
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc
%include base.inc

%define _prefix /usr
%define tarball_version  20100424-3.0
%define tarball_name	 libedit

Name:                    SFEeditline
IPS_package_name:	 library/editline
Summary:                 A command line editing and history library
Version:                 3.0
License:		 BSDL
Url:                     http://www.thrysoee.dk/editline/
Source:                  http://www.thrysoee.dk/editline/%{tarball_name}-%{tarball_version}.tar.gz
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

# OpenSolaris IPS Package Manifest Fields
Meta(info.maintainer):	 	taki@justplayer.com
Meta(info.upstream):	 	http://www.thrysoee.dk/editline/
# Meta(info.repository_url):	[open source code repository]
Meta(info.classification):	System Libraries

BuildRequires: SUNWhea
BuildRequires: system/library
Requires: system/library

%description
This is an autotool- and libtoolized port of the NetBSD Editline library (libedit). This Berkeley-style licensed command line editor library provides generic line editing, history, and tokenization functions, similar to those found in GNU Readline.

%prep
%setup -c -n %{tarball_name}-%{tarball_version}

%ifarch amd64 sparcv9
rm -rf %{tarball_name}-%{tarball_version}-64
cp -rp %{tarball_name}-%{tarball_version} %{tarball_name}-%{tarball_version}-64
%endif

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{tarball_name}-%{tarball_version}
%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure \
 --prefix=%{_prefix}\
 --sysconfdir=%{_sysconfdir} \
 --libdir=%{_libdir} \
 --bindir=%{_bindir} \
 --includedir=%{_includedir} \
 --mandir=%{_mandir}

gmake -j$CPUS 

%ifarch amd64 sparcv9
export CFLAGS
cd ../%{tarball_name}-%{tarball_version}-64

export CFLAGS="-m64 -i -xO4 -xspace -xstrconst -fast -Kpic -xregs=no%frameptr -xc99=none -xCC"
export CXXFLAGS="-m64 -i -xO4 -xspace -xstrconst -fast -Kpic -xregs=no%frameptr -xc99=none -xCC"
export LDFLAGS="%_ldflags"
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

%endif


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, bin) %{_prefix}/include
%{_prefix}/include/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
* Wed Feb 16 17:16:29 JST 2011  TAKI, Yasushi <taki@justplayer.com>
- support 64bit.
- use studio12
- rename editline to SFEeditline
* Tue Jan  5 16:49:53 JST 2010  TAKI, Yasushi <taki@justplayer.com>
- Initial Revision
