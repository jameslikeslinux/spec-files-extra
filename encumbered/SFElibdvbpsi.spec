#
# spec file for package SFElibdvbpsi
#
# includes module(s): libdvbpsi
#
%include Solaris.inc
%define srcname libdvbpsi

Name:                    SFElibdvbpsi
IPS_Package_Name:	 library/video/libdvbpsi 
Summary:                 A simple library designed for decoding and generation of MPEG TS and DVB PSI tables
URL:                     http://www.videolan.org/developers/libdvbpsi.html
Version:                 0.2.2
License:	LGPL2.1
Source:                  http://download.videolan.org/pub/%srcname/%version/%srcname-%version.tar.bz2
Patch1:			 libdvbpsi-01-configure.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LIBS=-lxnet
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-release

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/*


%changelog
* Sat Aug 18 2012 - Milan Jurik
- bump to 0.2.2
* Wed Feb 02 2011 - Alex Viskovatoff
- update to 0.1.7; use configure --enable-release
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibdvbpsi
- changed to root:bin to follow other JDS pkgs.
* Wed Feb 15 2004 - glynn.foster@sun.com
- Initial version
