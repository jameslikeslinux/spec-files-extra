# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	gdal
%define src_version	1.8.0
%define pkg_release	1

# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	GDAL - Geospatial Data Abstraction Library
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	X/MIT
Group:          Library
Source:         http://download.osgeo.org/gdal/%{src_name}-%{version}.tar.gz
Vendor:       	http://www.gdal.org
URL:            http://www.gdal.org
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

Requires: SFEgcc
Requires: SFElibgeotiff
BuildRequires: SFEgcc
BuildRequires: SFElibgeotiff

%description 
GDAL - Geospatial Data Abstraction Library


%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
#%patch1 -p1

CC=gcc
CXX=g++
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}

# sh==bash is extremely hardcoded. Yes, I used the phrase "extremely hardcoded".
# It is that bad.
sed -e 's/$(SHELL)/\/bin\/bash/' GDALmake.opt > GDALmake.opt.new
mv GDALmake.opt.new GDALmake.opt


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
make

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File permissions, ownership information. Note the difference between 
# bin(_bindir),share(_datadir) & share/applications
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gdal

#%dir %attr (0755, root, bin) %{_mandir}
#%{_mandir}/*

#%dir %attr (0755, root, bin) %{_libdir}/python2.4
#%{_libdir}/python2.4/site-packages/*


%changelog
* Thu Feb 24 2011 - jchoi42@pha.jhu.edu
- Bump to 1.8.0. 
- Add devel pkg. Specify shell, dependencies.
* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
