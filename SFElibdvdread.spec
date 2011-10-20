#
# spec file for package SFElibdvdread
#
# includes module(s): libdvdread
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:                    SFElibdvdread
Summary:                 Library for reading DVD video disks
Version:                 4.2.0
License:                 GPLv2+
SUNW_Copyright:	         libdvdread.copyright
URL:                     http://dvdnav.mplayerhq.hu
Source:                  http://dvdnav.mplayerhq.hu/releases/libdvdread-%{version}.tar.bz2
Patch1:			 libdvdread-01-dvdfilestat.diff
Patch2:			 libdvdread-02-wall.diff
SUNW_BaseDir:            %{_basedir}
buildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#BuildRequires:           SFEgcc
#Requires:                SFEgccruntime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libdvdread-%version
#%patch1 -p1
#%patch2 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
libtoolize
aclocal -I m4
autoheader
automake -a -f -c
autoconf -f
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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*


%changelog
* Thu Oct 20 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 4.2.0
* Fri Jul 22 2011 - Alex Viskovatoff
- Build with gcc, so that mplayer2 can play DVDs
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Fri Apr 15 2011 - Alex Viskovatoff
- Update source URL
* Mon Mar 15 2010 - Albert Lee <trisk@opensolaris.org>
- Remove SFElibdvdcss dependencies
- Update source URL
* Tue Sep 15 2009 - Thomas Wagner
- fix permissions for /usr/share aka %dir %attr (0755, root, sys) %{_datadir}
* Fri Sep 11 2009 - drdoug007@gmail.com
- Added dvdfilestat patch and encouraged allowed a gcc build
* Sat Jun 13 2009 - Milan Jurik
- new upstream, version 4.1.3
* Sat Jun 14 2008 - trisk@acm.jhu.edu
- Update download link
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibdvdread
- changed to root:bin to follow other JDS pkgs.
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
