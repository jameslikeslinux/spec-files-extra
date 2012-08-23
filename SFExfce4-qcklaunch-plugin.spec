# Initial spec for xfce4-quicklauncher-plugin by Ken Mays
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define src_name xfce4-quicklauncher-plugin

Name:			SFExfce4-qcklaunch-plugin
Summary:		Plugin QuickLauncher Plugin for Xfce
Version:		1.9.4
URL:			http://goodies.xfce.org/projects/panel-plugins/quicklauncher-plugin
Source0:		http://archive.xfce.org/src/panel-plugins/xfce4-quicklauncher-plugin/1.9/xfce4-quicklauncher-plugin-%{version}.tar.bz2 
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		SFElibxfcegui4-devel
Requires:		SFElibxfcegui4
BuildRequires:		SFExfce4-panel-devel
Requires:		SFExfce4-panel
Requires:		SUNWpostrun

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
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
%{_libdir}
%{_datadir}

%changelog
* Sat Oct 8 2011 - Ken Mays <kmays2000@gmail.com>
- Initial version (1.9.4)
