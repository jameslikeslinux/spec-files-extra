#
# Initial GVFS Mount plugin spec by Ken Mays
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define src_name xfce4-gvfs-mount

Name:       		SFExfce4-gvfs-mount
Version:    		0.0.4-6d2684b
Summary:    		Xfce4 GVfs Mount for the Xfce panel
Group:      		User Interface/Desktops
License:    		GPLv2+
URL:        		http://goodies.xfce.org/projects/panel-plugins/
Source0:    		http://archive.xfce.org/src/panel-plugins/xfce4-gvfs-mount/0.0/xfce4-gvfs-mount-0.0.4-6d2684b.tar.bz2	
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/xfce4-gvfs-plugin-%{version}
BuildRequires:          SFElibxfcegui4-devel
Requires:               SFElibxfcegui4
BuildRequires:          SFExfce4-panel-devel
Requires:               SFExfce4-panel
Requires:               SUNWpostrun
 
%description
Xfce4 GVfs Mount is a small application that is meant to mount remote file systems only.
 
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
%doc AUTHORS COPYING ChangeLog README
%{_libdir}
%{_bindir}
%{_datadir}/xfce4/panel-plugins/*.desktop
%{_datadir}/dbus-1/services/*
%{_datadir}/xfce4-gvfs-mount/glade/* 
%{_datadir}/locale/*

%changelog
* Fri Oct 7 2011 - Ken Mays <kmays2000@gmail.com>
- Initial version
