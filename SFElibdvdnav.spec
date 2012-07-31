#
# spec file for package SFElibdvdnav
#
# includes module(s): libdvdnav
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:                    SFElibdvdnav
IPS_Package_Name:	 library/video/libdvdnav 
Summary:                 DVD navigation library
Version:                 4.2.0
License:                 GPLv2+
SUNW_Copyright:	         libdvdnav.copyright
URL:                     http://dvdnav.mplayerhq.hu
Source:                  http://dvdnav.mplayerhq.hu/releases/libdvdnav-%{version}.tar.bz2
Patch1:                  libdvdnav-01-Wall.diff
SUNW_BaseDir:            %{_basedir}
buildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibdvdread

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
BuildRequires: SFElibdvdread-devel

%prep
%setup -q -n libdvdnav-%version
%patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ."
export PKG_CONFIG_PATH="/usr/lib/pkgconfig:/usr/share/pkgconfig:%{_libdir}/pkgconfig"
export PATH="$PATH:%{_bindir}"


libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dvdnav-config
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Oct 20 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 4.2.0
* Mon Oct 10 2011 - Milan Jurik
- add IPS package name
* Fri Jul 22 2011 - Alex Viskovatoff
- Build with gcc, so that mplayer2 can play DVDs
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Fri Apr 15 2011 - Alex Viskovatoff
- Update source URL
* Mon Mar 15 2010 - Albert Lee <trisk@opensolaris.org>
- Update source URL
* Mar 2010 - Gilles Dauphin
- want an install in /usr/SFE (_basedir)
* Sat Jun 13 2009 - Milan Jurik
- upgrade to 4.1.3
* Tue Sep 02 2008 - halton.huo@sun.com
- Add /usr/share/aclocal to ACLOCAL_FLAGS to fix build issue
* Tue Jul 22 2008 - trisk@acm.jhu.edu
- Update to 4.1.2
* Sun Jan  7 2007 - laca@sun.com
- create
