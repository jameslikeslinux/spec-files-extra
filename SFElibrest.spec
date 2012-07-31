#
# spec file for package SFElibrest
#
# includes module(s): librest
#

%include Solaris.inc
Name:		SFElibrest
IPS_Package_Name:	system/library/librest
License:	LGPL v2
Group:		Libraries/Multimedia
Version:	0.7.11
Summary:	Interface to access RESTful web services.
Source:		http://ftp.gnome.org/pub/GNOME/sources/rest/0.7/rest-%{version}.tar.bz2
Patch1:		librest-01-wall.diff
Patch2:		librest-02-example.diff
URL:		http://live.gnome.org/Librest
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:	%{_basedir}

%include default-depend.inc
Requires:	SUNWglib2
Requires:	SUNWlibsoup
BuildRequires:	SUNWglib2-devel
BuildRequires:	SUNWlibsoup-devel

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
%setup -q -n rest-%version
%patch1 -p1
%patch2 -p1

%build
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--libdir=%{_libdir}	\
	--bindir=%{_bindir}	\
	--libexecdir=%{_libexecdir} \
	--mandir=%{_mandir}	\
	--enable-introspection=no
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Sat Oct 29 2011 - Milan Jurik
- bump to 0.7.11
* Sun Oct 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created with version 0.6
