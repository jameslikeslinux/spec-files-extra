#
# spec file for package gnome-js-common
#
# Copyright (c) 2010 Sun Microsystems, Inc.
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc

%define	src_name gnome-js-common

Summary:	Common modules for GNOME JavaScript bindings
Name:		SFEgnome-js-common
IPS_Package_Name:	library/gnome/js-common
Version:	0.1.2
License:	GPLv3
Group:		Libraries
Source:		http://ftp.gnome.org/pub/GNOME/sources/gnome-js-common/0.1/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
This package provides common modules for GNOME JavaScript bindings.

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi


intltoolize --copy --force --automake
libtoolize --force
aclocal 
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --libexecdir=%{_libexecdir}		\
	    --localstatedir=%{_localstatedir}   \
	    --mandir=%{_mandir}			


make -j $CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_libdir}/gnome-js
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Sun Nov 20 2011 - Milan Jurik
- clean up
* Tue Sep 07 2010 - <yuntong.jin@sun.com>
- Init spec file
