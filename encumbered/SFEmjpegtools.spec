#
# spec file for package SFEmjpegtools
#
# includes module(s): SFEmjpegtools
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:		SFEmjpegtools
IPS_Package_Name:	video/mjpegtools
Summary:	mjpegtools - MPEG tools
Version:	2.0.0
Source:		%{sf_download}/mjpeg/mjpegtools-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWwxwidgets
BuildRequires: SFElibquicktime-devel
Requires: SFElibquicktime
BuildRequires: SFElibdv-devel
Requires: SFElibdv

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n mjpegtools-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%_ldflags -L/usr/X11/lib -L/usr/sfw/lib -R/usr/X11/lib -R/usr/sfw/lib"
export CPPFLAGS="-I/usr/X11/include -I/usr/sfw/include"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
	    --infodir=%{_datadir}/info       \
            --enable-shared		     \
	    --disable-static                 

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/info
%{_datadir}/man

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Nov 20 2011 - Milan Jurik
- add libdv
- add IPS package name
- bump to 2.0.0
- back to GCC because of templates mess
* Wed Sep 09 2009 - Milan Jurik
- update to 1.9.0
- switch to Sun CC
- SUNWwxwidgets used
* Fri Feb 16 2007 - dougs@truemail.co.th
- Removed -j from make
* Tue Nov 28 2006 - laca@sun.com
- make it work with either SFEwxwidgets or SFEwxGTK
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
