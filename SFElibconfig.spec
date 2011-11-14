#
# spec file for package SFElibmaa
#
# includes module: libmaa
#

%include Solaris.inc
%define srcname libconfig

Name:		SFElibconfig
Summary:	Simple library for processing structured configuration files
Group:		System/Libraries
URL:		http://www.hyperrealm.com/libconfig/
Version:	1.4.8
#License:	LGPLv2+
#SUNW_Copyright:	libmaa.copyright
Source:		http://www.hyperrealm.com/%srcname/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc


%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%_prefix --disable-static

gmake -j$CPUS


%install
rm -rf %buildroot
gmake install DESTDIR=%buildroot
rm %buildroot%_libdir/*.la
rm %buildroot%_datadir/info/dir

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_libdir
%_libdir/libconfig*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/libconfig.h*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%_libdir/pkgconfig/*
%dir %attr (0755, root, sys) %_datadir
%_datadir/info

%changelog
* Mon Aug 29 2011 - Alex Viskovatoff
- Initial spec
