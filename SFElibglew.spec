#
# spec file for package SFElibglew
#
# includes module(s): glew
#
#
%include Solaris.inc

%define src_name glew

Summary:	OpenGL Extension Wrangler Library
IPS_Package_Name:	x11/library/glew
Name:		SFElibglew
Version:	1.7.0
License:	BSD
Group:		Development/Libraries
URL:		http://glew.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tgz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWxorg-mesa
Requires:	SUNWxorg-mesa

%description
The OpenGL Extension Wrangler Library (GLEW) is a cross-platform C/C++ 
extension loading library. GLEW provides efficient run-time mechanisms 
for determining which OpenGL extensions are supported on the target 
platform. OpenGL core and extension functionality is exposed in a single 
header file.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name}

%description devel
This package contains the header files, static libraries and development
documentation for glew. If you like to develop programs using glew,
you will need to install %{name}-devel.

%prep
%setup -q -n %{src_name}-%{version}

%build
make LDFLAGS.EXTRA="-lc"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
make GLEW_DEST=$RPM_BUILD_ROOT%{_prefix} install

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_libdir}/libGLEW.so.*

%files devel
%defattr(-, root, bin)
%{_includedir}/GL/*.h
%{_libdir}/libGLEW.so
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Feb 12 2012 - Milan Jurik
- bump to 1.7.0
* Sat Mar 05 2011 - Milan Jurik
- bump to 1.5.8
* Sun Dec 19 2010 - Milan Jurik
- bump to 1.5.7
* Sat May 15 2010 - Milan Jurik
- Initial package
