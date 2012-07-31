# Initial spec for Xfce Sensors plugin
# By Ken Mays
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc


Name:			SFExfce4-sensors-plugin
Summary:		Hardware sensors plugin for the Xfce panel
Version:		1.2.3
URL:			http://goodies.xfce.org/projects/panel-plugins/xfce4-sensors-plugin
Source0:		http://archive.xfce.org/src/panel-plugins/xfce4-sensors-plugin/1.2/xfce4-sensors-plugin-%{version}.tar.bz2		
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/sensors-plugin-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
Requires:		SUNWpcre
BuildRequires:		SFElibxfcegui4-devel
Requires:		SFElibxfcegui4
BuildRequires:		SFExfce4-panel-devel
Requires:		SFExfce4-panel
Requires:		SUNWpostrun

%prep
%setup -q -n xfce4-sensors-plugin-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -lsocket -lnsl"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-gtk-doc \
            --disable-static
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_datadir}
%{_bindir}/*
%{_libdir}/xfce4/*
%{_libdir}/pkgconfig/libxfce4sensors-1.0.pc
%{_datadir}/applications/xfce4-sensors.desktop
%{_datadir}/xfce4/panel-plugins/xfce4-sensors-plugin.desktop
%{_datadir}/icons/hicolor/*/apps/xfce-sensors.png
%{_datadir}/icons/hicolor/scalable/apps/xfce-sensors.svg
%defattr(0755,root,bin)
%{_datadir}/locale*

%changelog
* Fri Oct 7 2011 - Ken Mays <kmays2000@gmail.com>
- Initial version
