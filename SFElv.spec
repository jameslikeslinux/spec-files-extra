#
# spec file for package lv
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc

%define _prefix /usr
%define tarball_version 451

Name:                    SFElv
IPS_package_name:        text/lv
Summary:                 a Powerful Multilingual File Viewer / Grep
Version:                 4.51
License:		 GPLv2
Url:                     http://www.ff.iij4u.or.jp/~nrt/lv/
Source:                  http://www.ff.iij4u.or.jp/~nrt/freeware/lv%{tarball_version}.tar.gz
Patch1:                  %{name}-01-kohju.diff
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


# OpenSolaris IPS Package Manifest Fields
Meta(info.maintainer):	 	pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):	 	NARITA Tomio <nrt@ff.iij4u.or.jp>
# Meta(info.repository_url):	[open source code repository]
Meta(info.classification):	System Utilities

%description
lv is a powerful multilingual file viewer. Apparently, lv looks like less (1), a representative file viewer on UNIX as you know, so UNIX people (and less people on other OSs) don't have to learn a burdensome new interface. lv can be used on MSDOS ANSI terminals and almost all UNIX platforms. lv is a currently growing software, so your feedback is welcome and helpful for us to refine the future lv. 

%prep
%setup -c -n %name-%version
cd lv%{tarball_version}
gtar zxvf %SOURCE0
%patch1 -p1

#%ifarch amd64 sparcv9
#cd ..
#rm -rf %{name}%{tarball_version}-64
#cp -r %{name}%{tarball_version} %{name}%{tarball_version}-64
#%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="%_ldflags"
export CC=cc

cd lv%{tarball_version}/build

%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

../src/configure --prefix=%{_prefix}
gmake -j$CPUS

#%ifarch amd64 sparcv9
#cd ../../%{name}%{tarball_version}-64/build
#export CFLAGS="%optflags64"
#../src/configure --prefix=%{_prefix}
#gmake -j$CPUS
#%endif

%install
#%ifarch amd64 sparcv9
#cd tiff-%{tarball_version}-64
#make install DESTDIR=$RPM_BUILD_ROOT
#if test -d sun-manpages; then
#	cd sun-manpages
#	make install DESTDIR=$RPM_BUILD_ROOT
#	cd ..
#fi
#rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
#cd ..
#%endif

cd lv%{tarball_version}/build
make install DESTDIR=$RPM_BUILD_ROOT
if test -d sun-manpages; then
	cd sun-manpages
	make install DESTDIR=$RPM_BUILD_ROOT
	cd ..
fi

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:lv:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/lib*.so*
#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%attr (0755, root, bin) %{_libdir}/%{_arch64}/lib*.so*
#%endif
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Tue May  5 2009 TAKI, Yasushi <taki@justplayer.com>
- updated to 1.0.0
