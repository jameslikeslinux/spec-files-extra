#
# spec file for package SFEqhull
#
# includes module(s): qhull
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use qhull = qhull.spec

Name:                    SFEqhull
IPS_Package_Name:	 library/desktop/g++/qhull
Summary:                 Implements the Quickhull algorithm
Group:                   Desktop (GNOME)/Libraries
License:                 BSD    
Version:                 %{qhull.version}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEgcc
#BuildRequires: SFEsigcpp-gpp-devel


%description
Qhull computes the convex hull, Delaunay triangulation, Voronoi diagram, 
halfspace intersection about a point, furthest-site Delaunay 
triangulation, and furthest-site Voronoi diagram. It runs in 2-d, 3-d, 
4-d, and higher dimensions. It implements the Quickhull algorithm for 
computing the convex hull. Qhull handles roundoff errors from floating 
point arithmetic. It can approximate a convex hull.

%prep
rm -rf %name-%version
mkdir %name-%version
%qhull.prep -d %name-%version

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags -fno-strict-aliasing"
export LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib"
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"
%qhull.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

# Actually this does nothing. Need to manually change in base-specs
export prefixdir=%{_prefix}

%qhull.install -d %name-%version

# Contrary to documentation, setting BINDIR, LIBDIR, etc do nothing.
# Manually move everything to less obnoxious locations.
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mv $RPM_BUILD_ROOT/$prefixdir/man/* $RPM_BUILD_ROOT/%{_mandir}
rm -r $RPM_BUILD_ROOT/$prefixdir/man/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %dir %{_docdir}
%{_docdir}/packages/qhull/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Fri Jan 13 2012 - James Choi
- Initial spec
