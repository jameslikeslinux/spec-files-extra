#
# Initial XFCE Battery plugin spec by Ken Mays
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define src_name xfce4-battery-plugin

Name:       		SFExfce4-battery-plugin
Version:    		1.0.0
Summary:    		Battery monitor for the Xfce panel
Group:      		User Interface/Desktops
License:    		GPLv2+
URL:        		http://goodies.xfce.org/projects/panel-plugins/
Source0:    		http://archive.xfce.org/src/panel-plugins/xfce4-battery-plugin/1.0/xfce4-battery-plugin-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/xfce4-battery-plugin-%{version}
BuildRequires:          SFElibxfcegui4-devel
Requires:               SFElibxfcegui4
BuildRequires:          SFExfce4-panel-devel
Requires:               SFExfce4-panel
Requires:               SUNWpostrun
 
%description
A battery monitor plugin for the Xfce panel, compatible with APM and ACPI.
 
%prep
%setup -q -n %{src_name}-%{version}

 
%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -lsocket -lnsl"
export LDFLAGS="%_ldflags"

%configure ./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
	    --disable-static
make -j $CPUS
 
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
 
%post
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
 
%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
 
%clean
rm -rf $RPM_BUILD_ROOT
 
%files 
%defattr(-,root,bin)
%doc AUTHORS COPYING COPYING.LIB ChangeLog README
%{_libexecdir}/xfce4/panel-plugins/xfce4-battery-plugin
%{_datadir}/xfce4/panel-plugins/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg 
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/locale/*

%changelog
* Fri Oct 7 2011 - Ken Mays <kmays2000@gmail.com>
- Initial version
