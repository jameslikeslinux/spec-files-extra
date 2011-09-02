#
# spec file for package SFEosg
#
#

%include Solaris.inc

%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc

%define src_name	OpenSceneGraph

%define SUNWcmake      %(/usr/bin/pkginfo -q SUNWcmake && echo 1 || echo 0)

Name:                   SFEosg
Summary:                High performance real-time graphics toolkit
Group:			Applications/Graphics
Version:                3.0.1
Source:                 http://www.openscenegraph.org/downloads/stable_releases/OpenSceneGraph-%{version}/source/OpenSceneGraph-%{version}.zip 
URL:			http:///www.openscenegraph.org/
#Patch9:			OpenSceneGraph-09-boost-concept-check.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

# <km> Note: Prefer >= cmake 2.8.4
BuildRequires:	SFEcmake

%description
The OpenSceneGraph is an OpenSource, cross platform graphics toolkit for the
development of high performance graphics applications such as flight
simulators, games, virtual reality and scientific visualization.
Based around the concept of a SceneGraph, it provides an object oriented
framework on top of OpenGL freeing the developer from implementing and
optimizing low level graphics calls, and provides many additional utilities
for rapid development of graphics applications.


%prep
%setup -q -c -n %{src_name}-%{version}
#%patch9 -p0

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}
export CC=/usr/gnu/bin/cc
export CXX=/usr/gnu/bin/g++
export CFLAGS="-I%_prefix/X11/include"
export CXXFLAGS="-I%_prefix/X11/include"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
export SDLMAIN_LIBRARY="/usr/lib"
export SDL_LIBRARY="SDL"
export CMAKE_LIBRARY_PATH="/opt/SFE/lib:/usr/lib"
export CMAKE_INCLUDE_PATH="/opt/SFE/include:/usr/include"
#SDLIMAGE_INCLUDE_DIR, SDLIMAGE_LIBRARY, SDL_INCLUDE_DIR, SDLMAIN_LIBRARY

mkdir -p BUILD
pushd BUILD

cmake -DSDL_LIBRARY="SDL" -DSDLMAIN_LIBRARY="/usr/lib" -DCMAKE_LIBRARY_PATH="/opt/SFE/lib:/usr/lib" -DCMAKE_INCLUDE_PATH="/opt/SFE/include:/usr/include" -DHAVE_GCC_VISIBILITY:INTERNAL=0 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DHAVE_VISIBILITY_SWITCH:INTERNAL=0 -DBUILD_OSG_EXAMPLES=ON -DBUILD_OSG_WRAPPERS=ON -DBUILD_DOCUMENTATION=ON ..

make VERBOSE=1 

#TODO
#make doc_openscenegraph doc_openthreads
popd

%install
cd %{src_name}-%{version}
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix}
pushd BUILD
#make install DESTDIR=${RPM_BUILD_ROOT}
make install
mv ./sfw_stage/* $RPM_BUILD_ROOT/%{_prefix}

# Supposed to take OpenSceneGraph data
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/OpenSceneGraph
popd


%clean
rm -rf $RPM_BUILD_ROOT

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
%{_datadir}/OpenSceneGraph/*
%{_includedir}/*

%changelog
* Fri Sep 02 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 3.0.1
- Built with oi_151 & GCC 4.6.1
* May 2010 - Gilles Dauphin
- Initial version
