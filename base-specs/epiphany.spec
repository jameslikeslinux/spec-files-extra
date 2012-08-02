#
# spec file for package epiphany
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#

%define revision 2.30

Name:         epiphany
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.30.6
Release:      4
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME web browser
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{revision}/%{name}-%{version}.tar.bz2
URL:          http://www.gnome.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

%prep
%setup -q

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export NSS_CFLAGS="-I/usr/include/mps"
export NSS_LIBS="-L/usr/lib/mps -R/usr/lib/mps -lnss3 -lplc4"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}		\
	--sysconfdir=%{_sysconfdir}	\
	--libexecdir=%{_libexecdir}	\
	--enable-seed			\
	--enable-introspection=yes	\
	--without-ca-file		\
	--enable-gtk-doc

make -j$CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Nov 20 2011 - Milan Jurik
- bump to 2.30.6
* Fri Feb 12 2010 - jchoi42@pha.jhu.edu
- bump to 2.28.2, remove depreciated patches, update patch 1 and 2
- update to _cxx_libdir, add %revision
* Wed Nov 07 2007 - damien.carbery@sun.com
- Initial version.
