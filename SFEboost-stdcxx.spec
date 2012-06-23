#
# spec file for package: [pkg name]
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): [pkg module(s)]
#
%define _basedir /usr/stdcxx
%include Solaris.inc
%define stl_is_stdcxx 1
%use boost = boost.spec

%include packagenamemacros.inc

%define	major 1
%define	minor 48
%define	patchlevel 0
%define ver_boost %{major}_%{minor}_%{patchlevel}

Name:		SFEboost-stdcxx
IPS_Package_Name:	system/library/stdcxx/boost
Summary:	Free peer-reviewed portable C++ libraries
Version:	%major.%minor.%patchlevel
License:	Boost Software License
URL:		http://www.boost.org/
Source:		%{sf_download}/boost/boost_%{ver_boost}.tar.bz2

SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc
BuildRequires: SFEicu-stdcxx-devel
BuildRequires: %{pnm_buildrequires_python_default}
Requires: SFEicu-stdcxx
Requires: SUNWlibstdcxx4

%package -n %name-devel
IPS_package_name:	system/library/stdcxx/boost/header-boost
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name

%package -n %name-doc
IPS_package_name:       system/library/stdcxx/boost/documentation
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

# It's not worth figuring out how to get the Boost build system
# to set the runpath correctly
%define rpath 'dyn:runpath /usr/stdcxx/lib'
pushd %{buildroot}%{_libdir}
for i in *.so.*; do
  elfedit -e %rpath $i
done
popd

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_libdir
%{_libdir}/lib*.so*

%files -n %name-devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%{_includedir}/boost
%{_libdir}/lib*.a

%files -n %name-doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/boost-%{version}

%changelog
* Sun Apr 29 2012 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_python_default}, %include packagenamacros.inc
* Sat Jan 14 2012 - Milan Jurik
- bump to 1.48.0
* Sun Apr  3 2011 - Alex Viskovatoff <herzen@imap.cc>
- Update to 1.46.1
* Thu Jan 27 2011 - Alex Viskovatoff
- Use -library=stdcxx4 instead of include/stdcxx.inc
* Wed Jan 26 2011 - Alex Viskovatoff
- Clean up CXXFLAGS
* Mon Jan 24 2011 - Alex Viskovatoff
- Use patches from KDE Solaris (other than the patch for sun.jam), to avoid
  duplication of effort
- Add -D_XOPEN_SOURCE=500 -D__EXTENSIONS__ to CXXFLAGS to make all targets build
- Create and use "feature.extend stdlib : sun-stdcxx" in sun.jam
* Sun Nov 28 2010 - Alex Viskovatoff
- Update to 1.45
- Remove -DPy_TRACE_REFS from CXXFLAGS, since it makes libboost_python.so
  incompatible with libpython2.6.so
* Sat Nov 20 2010 - Alex Viskovatoff
- Bump to 1.44 (filesystem library does not get built with 1.43)
- Use SFEicu, since library/icu is built against libcStd
- Use %stdcxx_cxxflags and %stdcxx_ldflags
- Do not package static libs
* Sat Aug 07 2010 - sobotkap@gmail.com
- Add patch to not link with stlport4
* Sun May 16 2010 - sobotkap@gmail.com
- Bump version to 1.43
* Wed Nov 04 2009 - sobotkap@gmail.com
- Bump version to 1.40.0
* Tue Oct 06 2009 - sobotkap@gmail.com
- Uncomment SUNWicud and add cpp flags for stdcxx.
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Comment out SUNWicud dependency to get module to build.
* Mon Aug 13 2007 - trisk@acm.jhu.edu
- Initial version
