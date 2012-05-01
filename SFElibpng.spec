# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc
%include usr-gnu.inc

%define src_name	libpng
%define src_version	1.5.10
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
IPS_Package_Name:	 image/library/libpng15
Summary:      	libpng - reference library for use in applications that create and manipulate PNG (Portable Network Graphics) raster image files
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	http://www.libpng.org/pub/png/src/libpng-LICENSE.txt
Source:         %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.bz2
Patch1:         libpng-01-no_ld_version_script.diff
URL:            http://www.libpng.org
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

%description 
libpng - reference library for use in applications that create and manipulate PNG (Portable Network Graphics) raster image files

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
%patch1 -p1

./configure --prefix=%{_prefix}

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
%{_libdir}/libpng*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, bin) %{_includedir}/libpng15
%{_includedir}/libpng15/*.h
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/man

%changelog
* Tue May 1 2012 - Logan Bruns <logan@gedanken.org>
- moved to /usr/gnu.
* Sun Apr 29 2012 - Logan Bruns <logan@gedanken.org>
- split out -devel package so runtime libs can be installed without conflicts
- bumped to 1.5.10
- fixed some permissions
* Sun Feb 26 2012 - Logan Bruns <logan@gedanken.org>
- Brought back and bumped to 1.4.9. This fixes security CVE-2011-3026 and with a rebuilt imagemagick support for PNG which is broken with the OI bundled libpng.
* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
