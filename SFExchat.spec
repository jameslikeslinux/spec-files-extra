#
# spec file for package SFExchat
#
# includes module: xchat
#

%include Solaris.inc
%define srcname xchat

Name:		SFE%srcname
Summary:	Multiplatform IRC client using GTK+
URL:		http://xchat.org/
Vendor:		Peter Železný <zed@xchat.org>
Version:	2.8.8
License:	LGPLv2.1
Source:		http://xchat.org/files/source/2.8/%srcname-%version.tar.bz2
SUNW_Copyright: xchat.copyright
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

# NOTE: There are probably other dependencies: feel free to add them.
# Probably it would be easiest to require something that pulls the usual
# OpenSolaris Gnome stuff in.
BuildRequires:	SUNWgtk2-devel
BuildRequires:	SUNWdbus-devel
Requires:	SUNWgtk2
Requires:	SUNWdbus
# desktop/irc/xchat is currently at 2.8.6, although IPS says it's 0.5.11
Conflicts:	SUNWxchat

Requires: %name-root
%package root
Summary:                 %summary - / filesystem
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

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# configure rejects the usual flags
#export CFLAGS=%optflags
#export LDFLAGS=%_ldflags

# Enabling Python breaks linking (ld: fatal: library -lutil: not found)
./configure --prefix=%_prefix -sysconfdir=%_sysconfdir --disable-python
gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%_datadir/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/%srcname
%_libdir/%srcname
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/applications
%attr (-, root, other) %_datadir/applications/%srcname.desktop
%_datadir/dbus-1
%dir %attr (-, root, other) %_datadir/pixmaps
%_datadir/pixmaps/%srcname.png

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %_sysconfdir
%dir %attr (0755, root, sys) %_sysconfdir/gconf
%dir %attr (0755, root, sys) %_sysconfdir/gconf/schemas
%attr (0755, root, sys) %_sysconfdir/gconf/schemas/apps_xchat_url_handler.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif


%changelog
* Mon Jul 25 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Sat Mar 12 2011 - Alex Viskovatoff
- Initial spec
