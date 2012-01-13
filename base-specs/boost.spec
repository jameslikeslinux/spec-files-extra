#
# spec file for package boost
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jchoi42
#

%define        major      1
%define        minor      48
%define        patchlevel 0
%define        ver_boost  %{major}_%{minor}_%{patchlevel}

%{!?boost_with_mt: %define boost_with_mt 0}

Name:         boost
License:      Boost License Version
Group:        System/Libraries
Version:      %{major}.%{minor}.%{patchlevel}
Summary:      boost - free peer-reviewed portable C++ source libraries
Source:       %{sf_download}/boost/boost_%{ver_boost}.tar.bz2
# Ticket #6161
Patch1:       boost-01-putenv.diff
Patch2:       boost-gpp-01-cstdint.diff
# Tickect #6131
Patch3:       boost-1.48.0-foreach.patch
URL:          http://www.boost.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}_%{major}_%{minor}_%{patchlevel}
%patch3	-p1
%if %cc_is_gcc
%patch2 -p0
%else
%patch1 -p0
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

BOOST_ROOT=`pwd`
%if %cc_is_gcc
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags"
%else
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
%endif

%if %cc_is_gcc
./bootstrap.sh --prefix=%{_prefix} --with-toolset=gcc --with-icu=/usr/g++
%else
./bootstrap.sh --prefix=%{_prefix} --with-toolset=sun --with-icu
%endif

./bjam --v2 -d+2 -q -j$CPUS -sBUILD="release <threading>single/multi" \
  release stage

%install
./bjam install --prefix=$RPM_BUILD_ROOT%{_prefix}

%changelog
* Thu Jan 12 2012 - Milan Jurik
- bump to 1.48.0
* Sat Jul 30 2011 - Milan Jurik
- bump to 1.47.0
* Thu Jun 23 2011 - Alex Viskovatoff
- enable ICU when building with gcc
* Sat Mar 19 2011 - Milan Jurik
- bump to 1.46.1 but disable graph lib for Sun Studio build
* Thu Aug 26 2010 - Brian Cameron <brian.cameron@oracle.com
- Bump to 1.44.
* Wed Aug 04 2010 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 1.43.
* Fri Mar 05 2010 - Brian Cameron <brian.cameron@sun.com>
- Bump to 1.42.
* Fri Jan 29 2010 - Brian Cameron <brian.cameron@sun.com>
- Add boost-with-mt option to build the mt version of the libraries.
  Do not build with ICU support if building the GCC version, otherwise the
  boost regex library is not usable.
* Wed Dec 02 2009 - Albert Lee <trisk@opensolaris.org>
- Add patch4 from upstream for #2602
- Update URL
* Mon Oct 12 2009 - jchoi42@pha.jhu.edu
- Bump to 1.40.0, updated boost-01-studio patch
- Initial base spec
