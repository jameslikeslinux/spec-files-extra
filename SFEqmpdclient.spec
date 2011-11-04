#
# spec file for package SFEqmpdclient
#
# includes module: qmpdclient
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname qmpdclient

Name:		SFEqmpdclient
Summary:	Qt4 based Music Player Daemon client
URL:		http://bitcheese.net/wiki/QMPDClient
License:	GPLv2
SUNW_Copyright:	%srcname.copyright
Group:		Applications/Sound and Video
Version:	1.2.2
Source:		http://dump.bitcheese.net/files/%srcname-%version.tar.bz2
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEgcc
BuildRequires:	SFEqt-gpp-devel
Requires:	SFEgccruntime
Requires:	SFEqt-gpp

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export PATH=/usr/g++/bin:$PATH
export CC=gcc
export CXX=g++
export CPPFLAGS="-I/usr/g++/include -I/usr/g++/include/qt"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads -fpermissive"
export LDFLAGS="%_ldflags -pthreads -lxnet -L/usr/g++/lib -R/usr/g++/lib"

sed "s|/usr/local|%buildroot%_prefix|" %srcname.pro > %srcname.pro.new
mv %srcname.pro.new %srcname.pro
sed 's|Qt;Network;Music;|AudioVideo;|' %srcname.desktop > %srcname.desktop.new
mv %srcname.desktop.new %srcname.desktop

qmake
make -j$CPUS


%install
rm -rf %buildroot
export PATH=/usr/g++/bin:$PATH

make install

%if %build_l10n
cp lang/*qm %buildroot%_datadir/QMPDClient/translations
%endif

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir/%srcname
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/%srcname.desktop
%dir %attr (-, root, other) %_datadir/icons
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/scalable
%dir %attr (-, root, other) %_datadir/icons/hicolor/scalable/apps
%_datadir/icons/hicolor/scalable/apps/%srcname.svg
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%_datadir/icons/hicolor/16x16/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22/apps
%_datadir/icons/hicolor/22x22/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48/apps
%_datadir/icons/hicolor/48x48/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64/apps
%_datadir/icons/hicolor/64x64/apps/%srcname.png

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, sys) %_datadir/QMPDClient
%attr (-, root, other) %_datadir/QMPDClient/translations/*.qm
%endif


%changelog
* Mon Aug  1 2011 - Alex Viskovatoff
- Initial spec
