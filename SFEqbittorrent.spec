#
# spec file for package SFEqbittorrent
#
# includes module: qbittorrent
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%define srcname qbittorrent

Name:		SFEqbittorrent
IPS_package_name: desktop/torrent/qbittorrent
Summary:	Free Software alternative to utorrent using Qt
Group:		Applications/Internet
URL:		http://qbittorrent.sourceforge.net/
Meta(info.upstream): Christophe Dumez <chris@qbittorrent.org>
License:	GPLv2
SUNW_Copyright:	%srcname.copyright
Group:		Applications/Internet
Version:	2.9.11
Source:		%sf_download/project/%srcname/%srcname/%srcname-%version/%srcname-%version.tar.gz
Patch1:		qbittorrent-01-filesystemwatcher.diff
Patch2:		qbittorrent-02-misc.diff

SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include	default-depend.inc

BuildRequires:	SFEgcc
BuildRequires:	SFEqt-gpp-devel
BuildRequires:	SFEboost-gpp-devel
BuildRequires:	SFElibtorrent-rasterbar-devel
Requires:	SFEgccruntime
Requires:	SFEqt-gpp
Requires:	SFEboost-gpp
Requires:	SFElibtorrent-rasterbar
Requires: 	%pnm_requires_python_default


%prep
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export PATH=/usr/g++/bin:$PATH
export QMAKESPEC=solaris-g++
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig
export CC=gcc
export CXX=g++
export CPPFLAGS="-I/usr/g++/include"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads"
export LDFLAGS="%_ldflags -pthreads -lxnet -L/usr/g++/lib -R/usr/g++/lib"

./configure --prefix=%_prefix --with-libboost-lib=/usr/g++/lib --with-libboost-inc=/usr/g++/include --qtdir=/usr/g++
make -j$CPUS


%install
rm -rf %buildroot

make install INSTALL_ROOT=%buildroot


%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir/%srcname
%dir %attr (-, root, sys) %_datadir
%_mandir
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/qBittorrent.desktop
%dir %attr (-, root, other) %_datadir/pixmaps
%_datadir/pixmaps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%_datadir/icons/hicolor/16x16/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22/apps
%_datadir/icons/hicolor/22x22/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24/apps
%_datadir/icons/hicolor/24x24/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/36x36
%dir %attr (-, root, other) %_datadir/icons/hicolor/36x36/apps
%_datadir/icons/hicolor/36x36/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48/apps
%_datadir/icons/hicolor/48x48/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64/apps
%_datadir/icons/hicolor/64x64/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/72x72
%dir %attr (-, root, other) %_datadir/icons/hicolor/72x72/apps
%_datadir/icons/hicolor/72x72/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/96x96
%dir %attr (-, root, other) %_datadir/icons/hicolor/96x96/apps
%_datadir/icons/hicolor/96x96/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128/apps
%_datadir/icons/hicolor/128x128/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/192x192
%dir %attr (-, root, other) %_datadir/icons/hicolor/192x192/apps
%_datadir/icons/hicolor/192x192/apps/%srcname.png


%changelog
* Sun Aug 05 2012 - Milan Jurik
- bump to 2.9.11
* Thu Oct 27 2011 - Alex Viskovatoff
- Update to 2.9.1, disabling one patch
- Add SUNW_copyright and IPS_package_name
* Tue Aug 30 2011 - Alex Viskovatoff
- Add missing dependency on Boost
* Sun Aug 28 2011 - Alex Viskovatoff
- Initial spec
