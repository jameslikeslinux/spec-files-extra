#
# package are under the same license as the package itself.
#
# bugdb: www.pulseaudio.org/report/
#
# Note that this requires building with the version 2.2.6b of libtool in 
# archive/SFElibtool.spec

%include Solaris.inc

%define src_name pulseaudio
%define src_url http://0pointer.de/lennart/projects/%{src_name}

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:		SFEpulseaudio
Summary:	pulseaudio - stream audio to clients
Version:	0.9.22
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		pulseaudio-01-default.pa.diff
# bug 254
Patch2:		pulseaudio-02-esdcompat.diff
# This patch is very rough, but gets the code to compile.
Patch3:         pulseaudio-03-solaris.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#TODO are dependencies complete? 
%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

BuildRequires: SUNWliboil-devel
BuildRequires: SFElibsamplerate-devel
Requires: SUNWliboil
Requires: SFElibsamplerate

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
IPS_package_name:        system/display-manager/gdm/l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir(relocate_from:%{_prefix}): %{_gnome_il10n_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
perl -pi -e 's,/bin/sh,/bin/ksh,' src/daemon/esdcompat.in

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#_XGP4_2 and __EXTENSIONS__ for rtp.c to find all typedefs
export CPPFLAGS="-D_XPG4_2 -D__EXTENSIONS__"

export CFLAGS="%gcc_optflags -std=c99"
export LDFLAGS="%{_ldflags} -lxnet -lsocket -lgobject-2.0"

# If you do not build with gcc, then it seems to need atomic_ops, and
# pulseaudio does not compile on Solaris with SFElibatomic-ops.  Should fix
# this so it can build with Sun Studio.
#
export CC=gcc

./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
#rm -f $RPM_BUILD_ROOT%{_libdir}/pulse-*/modules/lib*.a
#rm -f $RPM_BUILD_ROOT%{_libdir}/pulse-*/modules/lib*.la
find $RPM_BUILD_ROOT%{_libdir}/ -name "*.a" -exec rm {} \; -print -o -name  "*.la" -exec rm {} \; -print

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libexecdir}/pulse*
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/pulseaudio
%{_datadir}/vala
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0755, root, sys) %dir %{_sysconfdir}/pulse
%{_sysconfdir}/pulse/*
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/*

%{_sysconfdir}/xdg
%dir %attr (0755, root, bin) /lib
/lib/udev

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/*help/*/[a-z]*
%{_datadir}/omf/gdm/*-[a-z]*.omf
%endif

%changelog
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Tue Mar 04 2008 - trisk@acm.jhu.edu
- Add patch6 to fix pactl crash
* Sat Sep 22 2007 - Thomas Wagner
- add patch5 dirty_hack_IP_MULTICAST_LOOP-module-rtp-send.c
  TODO: find correct way to setup IP_MULTICAST_LOOP or isn't it necessary
* Tue Sep 18 2007 - trisk@acm.jhu.edu
- Add patch4
* Sat Sep 15 2007 - trisk@acm.jhu.edu
- Fix rules, add patch3
* Thu Sep 13 2007 - Thomas Wagner
- corrected rm lib*.a and lib*.la
- activated patch2 (default.pa)
* Tue Sep 04 2007 - Thomas Wagner
- Added LDFLAG -lsocket to solve ipv6 socket error when setting IP-ACLs
- remove left over files from lib/pulse-*/lib*\.a and \.la
- configuration-file default.pa: connection from mpd via 
  pulse-output now works. Listens to localhost, see examples
  for local LAN syntax
* Sun Aug 12 2007 - dougs@truemail.co.th
- Added ioctl patch and root package
* Tue May 22 2007 - Thomas Wagner
- Initial spec
