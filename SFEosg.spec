#
# spec file for package SFEosg
#
#

%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	OpenSceneGraph

Name:                   SFEosg
IPS_Package_Name:	library/osg
Summary:                High performance real-time graphics toolkit
Group:			Applications/Graphics
Version:                3.0.1
Source:                 http://www.openscenegraph.org/downloads/stable_releases/OpenSceneGraph-%{version}/source/OpenSceneGraph-%{version}.zip 
URL:			http:///www.openscenegraph.org/
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

# <km> Note: Prefer >= cmake 2.8.4
BuildRequires:	SFEcmake
BuildRequires:	SUNWgnuplot
BuildRequires:	SUNWdoxygen
BuildRequires:	SFEqt-gpp-devel
Requires:	SFEqt-gpp
BuildRequires:	SFEopenal-devel
Requires:	SFEopenal

%description
The OpenSceneGraph is an OpenSource, cross platform graphics toolkit for the
development of high performance graphics applications such as flight
simulators, games, virtual reality and scientific visualization.
Based around the concept of a SceneGraph, it provides an object oriented
framework on top of OpenGL freeing the developer from implementing and
optimizing low level graphics calls, and provides many additional utilities
for rapid development of graphics applications.


%prep
%setup -q -n %{src_name}-%{version}

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags} -I%{_includedir}"
export CXXFLAGS="%{cxx_optflags} -I%{_includedir}"
export LDFLAGS="%{_ldflags} -L%{_libdir} -R%{_libdir}"
export PATH=%{_bindir}:$PATH

mkdir -p build
cd build

cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_DOCUMENTATION=ON -DOPENTHREADS_ATOMIC_USE_MUTEX=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_RPATH=%{_libdir} ..

make -j$CPUS VERBOSE=1 

#TODO
#make doc_openscenegraph doc_openthreads

%install
rm -rf %{buildroot}

cd build
make install DESTDIR=%{buildroot}

# Supposed to take OpenSceneGraph data
mkdir -p %{buildroot}%{_datadir}/OpenSceneGraph


%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr(0755,root,bin) %{_libdir}
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%dir %attr(0755,root,bin) %{_libdir}/osgPlugins-%{version}
%dir %attr(0755,root,bin) %{_prefix}/doc/OpenThreadsReferenceDocs
%dir %attr(0755,root,bin) %{_prefix}/doc/OpenSceneGraphReferenceDocs
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_includedir}
%{_libdir}/lib*.so*
%{_libdir}/pkgconfig/*
%{_libdir}/osgPlugins-%{version}/*
%{_prefix}/doc/OpenThreadsReferenceDocs/*
%{_prefix}/doc/OpenSceneGraphReferenceDocs/*
%{_datadir}/OpenSceneGraph
%{_includedir}/*

%changelog
* Sun Feb 26 2012 - Milan Jurik
- fix build, move to /usr/g++
* Fri Sep 14 2011 - Thomas Wagner
- back to SFE default compiler location /usr/gnu/bin/gcc
  agreed with Ken on IRC
* Fri Sep 02 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 3.0.1
- Built with oi_151 & GCC 4.6.1
* May 2010 - Gilles Dauphin
- Initial version
