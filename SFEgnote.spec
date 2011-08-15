#
# spec file for package SFEgnote
#
# includes module: gnote
#

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define srcname gnote

Name:		SFEgnote
Summary:	Desktop notetaking application for Unix cloned from Tomboy
URL:		http://live.gnome.org/Gnote
License:	GPLv3
#SUNW_Copyright:	%srcname.copyright
Version:	0.7.5
Source:		http://ftp.gnome.org/pub/GNOME/sources/%srcname/0.7/%srcname-%version.tar.xz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEgcc
BuildRequires:	SFEboost-gpp-devel
BuildRequires:	SFEsigcpp-gpp-devel
BuildRequires:	SFEgtkmm-gpp-devel
BuildRequires:	SUNWgtkspell
BuildRequires:	SFEe2fsprogs
BuildRequires:	SFEpcre-gpp-devel
Requires:	SFEgccruntime
Requires:	SFEboost-gpp
Requires:	SFEsigcpp-gpp
Requires:	SFEgtkmm-gpp
Requires:	SUNWgtkspell
Requires:	SFEe2fsprogs
Requires:	SFEpcre-gpp

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CPPFLAGS="-I/usr/g++/include -I/usr/include/ext2fs -I/usr/include/pcre"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads"
export LDFLAGS="%_ldflags -pthreads -L/usr/gnu/lib -L/usr/lib/ext2fs -L/usr/g++/lib -R/usr/gnu/lib:/usr/lib/ext2fs:/usr/g++/lib"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig

./configure --prefix=%_prefix --sysconfdir=%_sysconfdir --with-boost=/usr/g++ --disable-static

make -j$CPUS


%install
rm -rf %buildroot

make install DESTDIR=%buildroot
rmdir %buildroot/usr/libexec
rm %buildroot/%_libdir/gnote/addins/%version/*.la

%if %build_l10n
%else
rm -rf %buildroot%_datadir/locale
cd %buildroot%_datadir/gnome/help
rm -r cs  de  el  es  fr  sl  sv  zh_CN
%endif

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir/%srcname
%_libdir/%srcname
%dir %attr (-, root, sys) %_datadir
%_datadir/%srcname
%_mandir
%dir %attr(0755, root, other) %_datadir/applications
%_datadir/applications/%srcname.desktop
%_datadir/omf/%srcname
%dir %attr(0755, root, other) %_datadir/gnome
%_datadir/gnome/help/%srcname/C

%files root
%defattr (-, root, sys)
%dir %attr (-, root, sys) %_sysconfdir
%%dir %attr (-, root, sys) %_sysconfdir/gconf
%dir %attr (-, root, sys) %_sysconfdir/gconf/schemas
%attr (-, root, sys) %_sysconfdir/gconf/schemas/%srcname.schemas

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
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24
%dir %attr (-, root, other) %_datadir/icons/hicolor/24x24/apps
%_datadir/icons/hicolor/24x24/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48/apps
%_datadir/icons/hicolor/48x48/apps/%srcname.png

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%dir %attr(0755, root, other) %_datadir/gnome
%_datadir/gnome/help/%srcname/cs
%_datadir/gnome/help/%srcname/de
%_datadir/gnome/help/%srcname/el
%_datadir/gnome/help/%srcname/es
%_datadir/gnome/help/%srcname/fr
%_datadir/gnome/help/%srcname/sl
%_datadir/gnome/help/%srcname/sv
%_datadir/gnome/help/%srcname/zh_CN
%endif


%changelog
* Sun Aug 14 2011 - Alex Viskovatoff
- Initial spec
