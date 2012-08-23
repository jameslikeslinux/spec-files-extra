#
# Initial xfce-clipman-plugin spec for Solaris 11 by Ken Mays
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1

Name:			SFExfce4-clipman-plugin
Summary:		Clipboard plugin for Xfce
Version:		1.1.3
URL:			http://goodies.xfce.org/projects/panel-plugins/xfce4-clipman-plugin
Source0:		http://archive.xfce.org/src/panel-plugins/xfce4-clipman-plugin/1.1/xfce4-clipman-plugin-%{version}.tar.bz2
Group:			User Interface/Desktops
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-component-devel
Requires:		SUNWgnome-component
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
BuildRequires:		SUNWgnome-panel-devel
Requires:		SUNWgnome-panel
BuildRequires:		SFElibxfcegui4-devel
Requires:		SFElibxfcegui4
BuildRequires:		SFElibxfce4util-devel
Requires:		SFElibxfce4util
BuildRequires:		SFExfce4-panel-devel
Requires:		SFExfce4-panel
Requires:		SUNWpostrun

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n xfce4-clipman-plugin-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-locales-dir=%{_datadir}/locale \
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
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u


%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/xfce4
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xfce4
%defattr(-,root,other)
%{_datadir}/icons
%{_datadir}/applications
%{_datadir}/locale

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/xdg/*

%changelog
* Wed Oct 5 2011 - Ken Mays <kmays2000@gmail.com>
- Initial version (v1.1.3)
