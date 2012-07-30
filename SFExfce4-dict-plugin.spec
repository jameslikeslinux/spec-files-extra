#
# Xfce Dict Plugin spec by Ken Mays
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define src_name xfce4-dict-plugin

Name:       		SFExfce4-dict-plugin
Version:    		0.3.0
Summary:    		Xfce4 Dict plugin for the Xfce panel
Group:      		User Interface/Desktops
License:    		GPLv2+
URL:        		http://goodies.xfce.org/projects/panel-plugins/
Source0:    		http://archive.xfce.org/src/panel-plugins/xfce4-dict-plugin/0.3/xfce4-dict-plugin-%{version}.tar.gz	
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/xfce4-dict-plugin-%{version}
BuildRequires:          SFElibxfcegui4-devel
Requires:               SFElibxfcegui4
BuildRequires:          SFExfce4-panel-devel
Requires:               SFExfce4-panel
Requires:               SUNWpostrun
 
%description
The xfce4-dict-plugin is now part of xfce4-dict, a client program to query different dictionaries. 
 
%prep
%setup -q -n %{src_name}-%{version}

 
%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -lsocket -lnsl"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
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
%{_datadir}/icons/hicolor/scalable/apps/dict-icon.svg
%{_datadir}/locale/*

%changelog
* Fri Oct 7 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 0.3.0, revised version 
* Tue Apr 10 2007 - dougs@truemail.co.th
- Added -lsocket and -lnsl to LDFLAGS
* Sun Mar 2 2007 - dougs@truemail.co.th
- Initial versionn
