# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name libxaw3dxft

Name:		SFElibxaw3dxft
IPS_Package_Name:	x11/library/toolkit/libxaw3dxft
Summary:	X Window toolkit library
Version:	1.3.3
URL:		http://sf-xpaint.sourceforge.net/
Source:		%{sf_download}/sf-xpaint/%{src_name}-%{version}.tar.bz2
Group:		System/Libraries
License:	MIT X
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
%include default-depend.inc
BuildRequires:	SUNWfreetype2
Requires:	SUNWfreetype2

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n %{src_name}-%{version}

%build

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} --disable-static
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_libdir}/*.so.*

%files devel
%defattr (-, root, bin)
%{_libdir}/*.so
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/X11

%changelog
* Sat Feb 18 2012 - Milan Jurik
- Initial spec
