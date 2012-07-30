#
# spec file for package SFEsmplayer2
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname lachs0r-SMPlayer2
%define pkgname smplayer2
%define gitrev	28e73b5
%define snapdate 20111026

Name:		SFEsmplayer2
IPS_package_name: media/smplayer2
Summary:	A fork of SMPlayer, targeted at mplayer2 users
Group:		Applications/Sound and Video
Meta(info.repository-url):	https://github.com/lachs0r/SMPlayer2
Meta(info.upstream):		Martin Herkt <lachs0r@srsfckn.biz>
Version:	0.0.0.%snapdate
License:	GPL
SUNW_Copyright:	smplayer.copyright
# Github stupidly names the zip snapshot file "master"
# We rename "master" to "%srcname-%gitrev.zip" by hand
#Source		 https://github.com/lachs0r/SMPlayer2/zipball/master
Source:		%srcname-%gitrev.zip
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc

BuildRequires:	SFEqt-gpp-devel
Requires:	SFEqt-gpp


%prep
%setup -q -n %srcname-%gitrev

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export PATH=/usr/g++/bin:$PATH
export QMAKESPEC=solaris-g++
export QTDIR=/usr/g++
gmake -j$CPUS PREFIX=%_basedir

%install
rm -rf $RPM_BUILD_ROOT

gmake install PREFIX=%_basedir DOC_PATH=%_docdir/%srcname DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/%pkgname
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/*.desktop
%_datadir/%pkgname
%dir %attr (-, root, other) %_datadir/icons
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%_datadir/icons/hicolor/16x16/apps/%pkgname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22/apps
%_datadir/icons/hicolor/22x22/apps/%pkgname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/%pkgname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64/apps
%_datadir/icons/hicolor/64x64/apps/%pkgname.png


%changelog
* Wed Oct 26 2011 - Alex Viskovatoff
- Fork spec for fork of smplayer off SFEsmplayer.spec
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Fri Jan 28 2011 - Alex Viskovatoff
- Stop linking to libCstd (which did not cause crashes for some reason)
- Add the Qt bin directory to $PATH, so one patch is no longer needed
* Thu Jan 27 2011 - Alex Viskovatoff
- Use SFEqt47, adding two patches
* Sun Oct 17 2010 - Alex Viskovatoff
- Initial spec
