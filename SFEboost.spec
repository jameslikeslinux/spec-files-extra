#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define stl_is_stdcxx 0
%use boost = boost.spec

Name:                SFEboost
IPS_Package_Name:	system/library/boost 
Summary:             Free peer-reviewed portable C++ source libraries
License:             Boost License Version
Group:		System/Libraries
URL:		http://www.boost.org/
SUNW_Copyright:      boost.copyright
Version:	     %{boost.version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWicud
BuildRequires: SUNWPython26
Requires: SUNWicu

%package devel
IPS_package_name:       system/library/boost/header-boost
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%package -n %name-doc
IPS_package_name:       system/library/boost/documentation
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%boost.prep -d %name-%version

%build
%boost.build -d %name-%version

%install
rm -rf %{buildroot}
%boost.install -d %name-%version

cd %{_builddir}/%name-%version/boost_%{boost.ver_boost}

mkdir -p %{buildroot}%{_docdir}/boost-%{version}
cd "doc/html"
for i in `find . -type d`; do
  mkdir -p %{buildroot}%{_docdir}/boost-%{version}/$i
done
for i in `find . -type f`; do
  cp $i %{buildroot}%{_docdir}/boost-%{version}/$i
done

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files -n %name-devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/boost
%{_libdir}/lib*.a

%files -n %name-doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/boost-%{version}

%changelog
* Sat May 19 2012 - Logan Bruns <logan@gedanken.org>
- added a missing define (stl_is_stdcxx) that is now need due to
  changes in the base spec.
* Thu Jan 12 2012 - Milan Jurik
- package restructuralization, static libs re-added
* Mon Oct 17 2011 - Milan Jurik
- add IPS package name
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Fri Jan 11 2011 - Milan Jurik
- do not deliver static libs
* Wed Dec 02 2009 - Albert Lee <trisk@opensolaris.org>
- Re-add SUNWicud
* Mon Oct 12 2009 - jchoi42@pha.jhu.edu
- changed %builddir, created base-specs/boost.spec
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Comment out SUNWicud dependency to get module to build.
* Mon Aug 13 2007 - trisk@acm.jhu.edu
- Initial version
