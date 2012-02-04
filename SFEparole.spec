#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name parole
%define src_url http://archive.xfce.org/src/apps/parole/0.2/

Name:       SFEparole
IPS_Package_Name:	xfce/media/parole
Summary:    Modern, Simple Media Player for the Xfce Desktop Environment 
Version:    0.2.0.6
Group:		Applications/Sound and Video
URL:        http://www.xfce.org/
Source:             %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:      SUNWgnome-base-libs-devel
Requires:           SUNWgnome-base-libs
BuildRequires:      SUNWdbus
BuildRequires:      SUNWgnome-media-devel
Requires:           SUNWgnome-media
BuildRequires:      SUNWlibnotify
Requires:           SUNWlibnotify
Requires:           SFEtaglib
BuildRequires:      SFElibxfce4util
BuildRequires:      SFElibxfcegui4 
Buildrequires:      SFExfce4-dev-tools
Requires:	    developer/documentation-tool/gtk-doc
Patch1:		    parole-0.2.0.6-add-uri-scheme-handler-support.diff
Patch2:             parole-0.2.0.6-fix-lib-linking-order.diff

%description
Parole is a modern simple media player based on the GStreamer framework
and written to fit well in the Xfce desktop. Parole features playback
of local media files, DVD/CD and live streams.  Parole is extensible
via plugins, for a complete how to write a plugin for Parole see the
Plugins API documentation and the plugins directory which contains
some useful examples.

%if %build_l10n
%package l10n
Summary:    %{summary} - l10n files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires:    %{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}
#%patch1 -p1
#%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

# GNU xgettext needed
export PATH=/usr/gnu/bin:$PATH
./configure --prefix=%{_prefix}        \
    --bindir=%{_bindir}        \
    --libdir=%{_libdir}        \
    --libexecdir=%{_libexecdir}    \
    --datadir=%{_datadir}        \
    --mandir=%{_mandir}        \
    --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

rm $RPM_BUILD_ROOT/%{_libdir}/parole-0/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin) 
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO 
%{_bindir}/parole 
%{_libdir}/parole-0/* 
%{_datadir}/parole/parole-plugins-0/*.desktop
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/parole.desktop 
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/parole.svg
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/parole.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/parole.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/parole.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/parole.png
%{_datadir}/parole/pixmaps/* 
%{_includedir}/parole/ 
#%{_datadir}/gtk-doc/html/Parole-Plugins 

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/locale
%attr (-, root, other) %_datadir/locale/*
%endif

%changelog
* Mon Jun 06 2011 - Ken Mays <kmays2000@gmail.com>
- Moved patch files to diff extensions.
* Mon Apr 25 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec for 0.2.0.6

