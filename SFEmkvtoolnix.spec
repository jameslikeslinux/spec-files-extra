#
# spec file for package SFEmkvtoolnix
#
# includes module: mkvtoolnix
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname mkvtoolnix
%define _pkg_docdir %_docdir/%srcname
%define with_SUNWruby %(pkginfo -q SFEruby && echo 0 || echo 1)

Name:		SFEmkvtoolnix
IPS_Package_Name:	media/mkvtoolnix
Summary:	Tools for the Matroska video container
Group:		Applications/Sound and Video
URL:		http://www.bunkus.org/videotools/mkvtoolnix
Meta(info.upstream):	Moritz Bunkus <moritz@bunkus.org>
Version:	5.7.0
License:	GPLv2
SUNW_Copyright:	mkvtoolnix.copyright
Source:		http://www.bunkus.org/videotools/%srcname/sources/%srcname-%version.tar.bz2
Patch5:		mkvtoolnix-05-terminal.diff

SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

%if %with_SUNWruby
BuildRequires: runtime/ruby-18
%endif

BuildRequires: SFEboost-gpp-devel
Requires: SFEboost-gpp
BuildRequires: SUNWlexpt
Requires: SUNWlexpt
BuildRequires: SUNWzlib
Requires: SUNWzlib
BuildRequires: SFElzo-devel
Requires: SFElzo
BuildRequires: SUNWogg-vorbis
Requires: SUNWogg-vorbis
BuildRequires: SUNWflac
Requires: SUNWflac
BuildRequires: SFEwxwidgets-gpp-devel
Requires: SFEwxwidgets-gpp

%description

MKVToolnix is a set of tools to create, alter and inspect Matroska files under
Linux, other Unices and Windows. They do for Matroska what the OGMtools do for
the OGM format and then some.

MKVToolnix consists of the tools mkvmerge, mkvinfo, mkvextract, and mkvpropedit.

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version
%patch5 -p1

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export USER_CXXFLAGS="%cxx_optflags -fpermissive -D_POSIX_PTHREAD_SEMANTICS"
export USER_LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
export ZLIB_CFLAGS="-I/usr/include"
export ZLIB_LIBS=-lz

CXXFLAGS=$USER_CXXFLAGS LDFLAGS=$USER_LDFLAGS ./configure --prefix=%_prefix \
--with-extra-includes=/usr/g++/include --with-boost-libdir=/usr/g++/lib \
--with-wx-config=/usr/g++/bin/wx-config
./drake -j$CPUS

%install
rm -rf %buildroot

./drake install DESTDIR=%buildroot

%if %build_l10n
%else
rm -rf %buildroot%_datadir/locale
rm -rf %buildroot%_docdir/%srcname/guide/zh_CN
%endif

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%dir %attr (-, root, other) %_docdir
%doc ChangeLog README AUTHORS
%_bindir
%dir %attr (-, root, sys) %_datadir
%_mandir
%_docdir/%srcname/guide
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/mkvinfo.desktop
%_datadir/applications/mkvmergeGUI.desktop
%dir %attr (-, root, root) %_datadir/mime
%dir %attr (-, root, root) %_datadir/mime/packages
%_datadir/mime/packages/%srcname.xml
%dir %attr (-, root, other) %_datadir/icons
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%_datadir/icons/hicolor/16x16/apps/*.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24/apps
%_datadir/icons/hicolor/24x24/apps/*.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/*.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48/apps
%_datadir/icons/hicolor/48x48/apps/*.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64/apps
%_datadir/icons/hicolor/64x64/apps/*.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/96x96
%dir %attr (-, root, other) %_datadir/icons/hicolor/96x96/apps
%_datadir/icons/hicolor/96x96/apps/*.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128/apps
%_datadir/icons/hicolor/128x128/apps/*.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/256x256
%dir %attr (-, root, other) %_datadir/icons/hicolor/256x256/apps
%_datadir/icons/hicolor/256x256/apps/*.png

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (-, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif

%changelog
* Sun Aug 05 2012 - Milan Jurik
- bump to 5.7.0
* Fri Oct 14 2011 - Alex Viskovatoff <herzen@imap.cc>
- Bump to 5.0.1
* Tue Aug  9 2011 - Alex Viskovatoff <herzen@imap.cc>
- Add missing (build) dependency
* Sat Jul 23 2011 - Alex Viskovatoff <herzen@imap.cc>
- Bump to 4.9.1; add SUNW_Copyright
* Mon Jul 18 2011 - Alex Viskovatoff <herzen@imap.cc>
- Modify CXXXFLAGS to enable building with gcc 4.6
* Thu Jun 23 2011 - Alex Viskovatoff <herzen@imap.cc>
- Build with g++
- Update to 4.8.0; build GUI
* Tue Apr 12 2011 - Alex Viskovatoff <herzen@imap.cc>
- Add patch to make build on oi_147
* Sun Apr  3 2011 - Alex Viskovatoff <herzen@imap.cc>
- Bump to 4.6.0
* Sat Feb  5 2011 - Alex Viskovatoff
- Update to 4.5.0, adding one patch and removing one no longer needed
* Thu Jan 27 2011 - Alex Viskovatoff
- Go back to using -library=stdcxx4 because SS 12u1 does indeed understand it
* Sun Nov 21 2010 - Alex Viskovatoff
- Update to 4.4.0, with two patches no longer required
- Accommodate to stdcxx libs and headers residing in /usr/stdcxx
- Do not use -library=stdcxx4, which Sun Studio 12u1 does not understand
* Thu Oct 21 2010 - Alex Viskovatoff
- Add patch kindly provided by Moritz Bunkus to fix runtime bug (number 567)
- Move out of experimental
* Sun Oct 10 2010 - Alex Viskovatoff
- Initial spec
