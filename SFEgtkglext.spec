# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	gtkglext
%define src_version	1.2.0

# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

Name:         	SFE%{src_name}
Summary:      	GtkGLExt is an OpenGL extension to GTK+ 2.0 or later
Version:      	%{src_version}
License:      	LGPL
Group:          System/Libraries
Source:         %{sf_download}/gtkglext/%{src_name}-%{version}.tar.bz2
URL:            http://gtkglext.sourceforge.net
Patch1:		gtkglext-01-modern.diff
BuildRoot:	%{_tmppath}/%{src_name}-%{version}-build
%include default-depend.inc

%description
GtkGLExt is an OpenGL extension to GTK+ 2.0 or later

%package devel
Summary:	%{summary} - development files
%include default-depend.inc

%prep 
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc/html/gtkglext

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/gtkglext-1.0/include
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Mon Feb 21 2011 - Milan Jurik
- fix packaging and linking error
* Sun Feb 20 2011 - Milan Jurik
- fix linking error with the latest GTK+
* Sun Oct 14 2007 - laca@sun.com
- rename to SFEgtkglext
- fix packaging
* Sat Aug 11 2007 - <shivakumar dot gn at gmail dot com>
- Initial spec.
