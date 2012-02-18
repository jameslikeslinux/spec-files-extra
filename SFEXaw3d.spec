#
# spec file for package: Xaw3d
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# include module(s): Xaw3d
#

%include Solaris.inc

%define src_name	libXaw3d

Name:           SFEXaw3d
IPS_Package_Name:	x11/library/toolkit/xaw3d
Summary:        X Window toolkit with 3D appearance
Version:        1.6.1
License:        X11
Source:         http://xorg.freedesktop.org/archive/individual/lib/%{src_name}-%{version}.tar.bz2
URL:            http://freshmeat.net/projects/xaw3d/
Group:          System/Libraries
Distribution:	OpenSolaris
Vendor:		OpenSolaris Community
%include default-depend.inc

BuildRequires:  SUNWxwopt
BuildRequires:  SUNWxwinc
BuildRequires:  SUNWbtool
BuildRequires:  SUNWgnu-coreutils

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   %{_basedir}
SUNW_Copyright: Xaw3d.copyright

%description 
Xaw3d is a general-purpose replacement for the Athena toolkit which
adds a 3D appearance and support for XPM images.

%package devel
Summary: Header files and static libraries for development using Xaw3d
Group: Development/X11

%prep
rm -rf %{src_name}-%{version}
%setup -q -n %{src_name}-%{version}

%build
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix} --disable-static

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}
%{_libdir}/*.so.*

%files devel
%defattr(-,root, bin)
%{_libdir}/*.so
%{_includedir}/X11/Xaw3d
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Feb 18 2012 - Milan Jurik
- fix deliverables
- bump to 1.6.1
* May 2010  - Gilles DAuphin
- import in SFE
- Name is SFE
* Sat Aug 29 2009 - bld
- touch file to initiate build
* Sat Aug 29 2009 - beffa at ieee dot org
- moved into real X11 directory
* Sat Jul 25 2009 - beffa at ieee dot org
- initial version
## Re-build 24/09/09
