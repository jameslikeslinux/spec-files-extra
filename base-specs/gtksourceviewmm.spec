#
# spec file for package cairomm 
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:                    gtksourceviewmm
License:		 LGPL
Group:			 System/Libraries
Version:                 2.10.2
Release:		 1
Summary:                 C++ API for gtksourceview
URL:                     http://projects.gnome.org/gtksourceviewmm/
Source:                  http://ftp.gnome.org/pub/GNOME/sources/%name/2.10/%name-%version.tar.xz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%package devel
Summary:                 %{summary} - development files

%prep
%setup -q -n %name-%version

%build

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} 	\
	    --disable-python 		\
	    --disable-docs
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%changelog
* Fri Aug  5 2011 - Alex Viskovatoff
- update to 1.8.6
* Tue Feb 19 2008 - ghee.teo@sun.com
- Modified according to review comments.
* Fri Feb 08 2008 - ghee.teo@sun.com
- Modified SFEcairomm.spec to make SUNWcairomm.spec and cairomm.spec
