#
# spec file for package ebview
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
%define tarball_version  0.3.6
%define tarball_name     ebview

Name:                    SFEebview
IPS_package_name:        desktop/dictionay/ebview
Summary:                 EPWING dictionary browser
Version:                 %{tarball_version}
License:		 GPLv2
Url:                     http://ebview.sourceforge.net/
Source:                  http://prdownloads.sourceforge.net/%{tarball_name}/%{tarball_name}-%{tarball_version}.tar.gz
Patch1:			 %{name}-01-kohju.diff
Patch2:			 %{name}-02-kohju.diff
Patch3:			 %{name}-03-kohju.diff
Patch4:			 %{name}-04-kohju.diff
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{tarball_name}-%{version}-build

# OpenSolaris IPS Package Manifest Fields
Meta(info.maintainer):	 	pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):	 	Kenichi Suto <deep_blue@users.sourceforge.net> , Hironori FUJII <fujii@chi.its.hiroshima-cu.ac.jp>
# Meta(info.repository_url):	[open source code repository]
Meta(info.classification):	Applications

Requires: library/eb
Requires: %{pnm_requires_SUNWhea}
Requires: %{pnm_requires_SUNWgnome_base_libs}
Requires: %{pnm_requires_SUNWxwrtl}
# Requires: %{pnm_requires_SUNWxwplt}
Requires: %{pnm_requires_SUNWlibms}
Requires: %{pnm_requires_SUNWmlib}
# Requires: %{pnm_requires_SUNWxorg_clientlibs}
Requires: %{pnm_requires_SUNWfontconfig}
Requires: %{pnm_requires_SUNWfreetype2}

BuildRequires: library/eb
BuildRequires: %{pnm_buildrequires_SUNWhea}
BuildRequires: %{pnm_buildrequires_SUNWgnome_base_libs}
BuildRequires: %{pnm_buildrequires_SUNWxwrtl}
# BuildRequires: %{pnm_buildrequires_SUNWxwplt}
BuildRequires: %{pnm_buildrequires_SUNWlibms}
BuildRequires: %{pnm_buildrequires_SUNWmlib}
# BuildRequires: %{pnm_buildrequires_SUNWxorg_clientlibs}
BuildRequires: %{pnm_buildrequires_SUNWfontconfig}
BuildRequires: %{pnm_buildrequires_SUNWfreetype2}
BuildRequires: %{pnm_buildrequires_SUNWbtool}
BuildRequires: %{pnm_buildrequires_SUNWbinutils}
BuildRequires: %{pnm_buildrequires_SUNWxcu4}
BuildRequires: %{pnm_buildrequires_SUNWgmake}
BuildRequires: x11/library/libpthread-stubs

%description
EPWING dictionary browser

%prep
%setup -c -n %name-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

#%ifarch amd64 sparcv9
#rm -rf %{tarball_name}-%{tarball_version}-64
#cp -rp %{tarball_name}-%{tarball_version} %{tarball_name}-%{tarball_version}-64
#%endif

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags} -lpangox-1.0"

cd %{tarball_name}-%{tarball_version}
%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

./configure \
 --prefix=%{_prefix} \
 --bindir=%{_bindir} \
 --with-eb-conf=%{_sysconfdir}/eb.conf \
 --with-x

gmake -j$CPUS

#%ifarch amd64 sparcv9
#cd ../%{tarball_name}-%{tarball_version}-64
#export CFLAGS="-m64"
#./configure \
# --prefix=%{_prefix}\
# --bindir=%{_bindir}/%{_arch64} \
# --with-eb-conf=%{_sysconfdir}/eb.conf \
# --with-x
#
#gmake -j$CPUS
#
#%endif

%install
cd %{tarball_name}-%{tarball_version}
gmake install DESTDIR=$RPM_BUILD_ROOT
cp -r pixmaps $RPM_BUILD_ROOT%{_prefix}/share/ebview/

if test -d sun-manpages; then
	cd sun-manpages
	make install DESTDIR=$RPM_BUILD_ROOT
	cd ..
fi

#%ifarch amd64 sparcv9
#cd ../%{tarball_name}-%{tarball_version}-64
#gmake install DESTDIR=$RPM_BUILD_ROOT
#cd ..
#%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{tarball_name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_prefix}/share
%attr(0755, root, other) %{_prefix}/share/*
#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/lib*.so*
#%endif

%changelog
* Wed May  6 2009 TAKI, Yasushi <taki@justplayer.com>
- Initial Revision
* Sat May 30 2009 TAKI, Yasushi <taki@justplayer.com>
- change for sourcejuicer.
* Tue Mar 29 2011 TAKI, Yasushi <taki@justplayer.com>
- initial revision for sfe.
* Tue Mar 29 2011 TAKI, Yasushi <taki@justplayer.com>
- Support eblib 4.3.1
