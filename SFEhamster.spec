#
# spec file for package SFEhamster
#
# includes module(s): hamster
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#


%include Solaris.inc
%include packagenamemacros.inc

%define srcname	hamster-applet

Name:                    SFEhamster
Summary:		 Time tracking for masses	
#Version:                 2.91.2 - needs new gnome?
#Version:                 2.32.1 - needs new gnome?
Version:                 2.24.3
#cut down to major.minor
%define version_major_minor %( echo %{version} | sed -e 's/\([0-9]*\.[0-9]*\)\..*/\1/' )
# 2.91.2
Source:                  http://ftp.gnome.org/pub/GNOME/sources/hamster-applet/%{version_major_minor}/hamster-applet-%{version}.tar.gz
URL:                     http://live.gnome.org/ProjectHamster
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:     %{pnm_buildrequires_SUNWsqlite3}
BuildRequires:     %{pnm_buildrequires_SUNWpysqlite}
BuildRequires:     %{pnm_buildrequires_SUNWlibC}
Requires:          %{pnm_buildrequires_SUNWsqlite3}
Requires:          %{pnm_requires_SUNWpysqlite}
Requires:          %{pnm_requires_SUNWlibC}

%prep
%setup -q -n hamster-applet-%{version}

#replace with explicit python version from %{python_major_minor_version}
perl -pi -e 's:^#! */usr/bin/python.*:#!/usr/bin/python%{python_major_minor_version}:' `find . -type f -print`
perl -pi -e 's:^#! */usr/bin/env *python:#!/usr/bin/python%{python_major_minor_version}2.6:' `find . -type f -print`

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

#NOTE: more fresh versions use different build/install system
%if %( test -x waf && echo 1 || echo 0 )
./waf --prefix=/usr configure build
%else
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
	    --bindir=%{_bindir}	\
	    --libdir=%{_libdir}	\
	    --mandir=%{_mandir}
make -j$CPUS
%endif


%install
rm -rf $RPM_BUILD_ROOT
#NOTE: more fresh versions use different build/install system
%if %( test -x waf && echo 1 || echo 0 )
./waf install --destdir=$RPM_BUILD_ROOT
%else
make DESTDIR=$RPM_BUILD_ROOT install
%endif

#NOTE: more fresh versions deliver binaries into /usr/bin
%if %( test -x $RPM_BUILD_ROOT/%{_bindir}/hamster-service )
%define has_binaries_in_usr_bin 1
%else
%define has_binaries_in_usr_bin 0
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/hamster-applet
%{_datadir}/hamster-applet/*
%dir %attr (0755, root, bin) %{_datadir}/gnome-control-center
%{_datadir}/gnome-control-center/*

#NOTE: more fresh versions deliver binaries into /usr/bin
%if %{has_binaries_in_usr_bin}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%endif
#END has_binaries_in_usr_bin
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/gconf
%dir %attr (0755, root, sys) %{_sysconfdir}/gconf/schemas
%{_sysconfdir}/gconf/schemas/*


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
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48/apps
%_datadir/icons/hicolor/48x48/apps/%srcname.png
#%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64
#%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64/apps
#%_datadir/icons/hicolor/64x64/apps/%srcname.png
#%dir %attr (-, root, other) %_datadir/icons/hicolor/72x72
#%dir %attr (-, root, other) %_datadir/icons/hicolor/72x72/apps
#%_datadir/icons/hicolor/72x72/apps/%srcname.png
#%dir %attr (-, root, other) %_datadir/icons/hicolor/96x96
#%dir %attr (-, root, other) %_datadir/icons/hicolor/96x96/apps
#%_datadir/icons/hicolor/96x96/apps/%srcname.png
#%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128
#%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128/apps
#%_datadir/icons/hicolor/128x128/apps/%srcname.png
     
##TODO## might be separated out in a build_l10n
%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale



%changelog
* Tue Apr 24 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} %{pnm_buildrequires_SUNWsqlite3} %{pnm_buildrequires_SUNWpysqlite} %{pnm_buildrequires_SUNWlibC}, %include packagenamemacros.inc
- Bump to 2.24.3
- fix permissions
- prepare for more recent build system, not yet used by 2.24.3
* Tue Nov 11 2008 - jijun.yu@sun.com
- Add BuildRequires.
* Wed Oct 22 2008 - jijun.yu@sun.com
- Bump to 2.24.1
* Tue Oct 07 2008 - jijun.yu@sun.com
- Initial spec
