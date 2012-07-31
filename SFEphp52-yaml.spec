#
# spec file for package eblib
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc
%include packagenamemacros.inc

%define _prefix /usr
%define tarball_version  1.0.1
%define tarball_name     yaml

Name:                    SFEphp52-yaml
IPS_package_name:	 web/php-52/extension/php-yaml
Summary:                 PHP 5.2 module for YAML
Version:                 1.0.1
License:		 PHP License
Url:                     http://pecl.php.net/package/%{tarball_name}
Source:                  http://pecl.php.net/get/%{tarball_name}-%{tarball_version}.tgz
Source1:                 %{name}.ini
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: %{pnm_buildrequires_SUNWphp52}
BuildRequires: %{pnm_buildrequires_SUNWgsed_devel}

Requires: %{pnm_requires_SUNWphp52}
Requires: SFElibyaml

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):	 	http://code.google.com/p/php-yaml/
Meta(info.maintainer):	 	taki@justplayer.com
Meta(info.classification):	Development/PHP

%prep
%setup -c -n %tarball_name-%tarball_version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="%_ldflags"
export CC=cc

cd %{tarball_name}-%{tarball_version}
%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

/usr/php/5.2/bin/phpize
./configure \
 --prefix=%{_prefix}\
 --exec-prefix=%{_prefix}\
 --sysconfdir=%{_sysconfdir} \
 --libdir=%{_libdir} \
 --bindir=%{_bindir} \
 --includedir=%{_includedir} \
 --mandir=%{_mandir} \
 --with-php-config=/usr/php/5.2/bin/php-config \
 --with-yaml=/usr

gmake -j$CPUS CFLAGS="$CFLAGS"
echo no | gmake test

%install

cd %{tarball_name}-%{tarball_version}
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/php/5.2/modules/
cp modules/yaml.so $RPM_BUILD_ROOT/%{_prefix}/php/5.2/modules/
mkdir -p  $RPM_BUILD_ROOT/etc/php/5.2/conf.d
cp %{SOURCE1} $RPM_BUILD_ROOT/etc/php/5.2/conf.d/%{tarball_name}.ini

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_prefix}
%dir %attr(0755, root, bin) %{_prefix}/php/5.2/modules
%{_prefix}/php/5.2/modules/*
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/php/5.2/conf.d/*

%changelog
* Sat Jun 25 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Initial Revision
