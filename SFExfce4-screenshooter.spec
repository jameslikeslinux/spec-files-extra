#
# spec file for package XFCE screenshooter 
#
# by Ken Mays
#
# http://goodies.xfce.org/projects/applications/xfce4-screenshooter

%include Solaris.inc

%define src_name xfce4-screenshooter
%define src_url http://archive.xfce.org/src/apps/xfce4-screenshooter/1.7/

Name:           SFExfce4-screenshooter
Summary:        An application to take screenshots
Version:        1.7.9
URL:            http://www.xfce.org/
Source:         %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SFElibxfcegui4 
BuildRequires:  SFElibxfce4ui
BuildRequires:  SFExfce4-panel
BuildRequires:  SUNWperl-xml-parser
Suggests:       xfce4-panel-plugin-screenshooter 
 
%description
Xfce4 Screenshooter allows you to capture the entire screen, the active window or a selected region. You can set the delay that elapses before the screenshot is taken and the action that will be done with the screenshot: save it to a PNG file, copy it to the clipboard, open it using another application, or host it on ZimageZ, a free online image hosting service. 

A plugin for the Xfce panel is also available. 

%package -n xfce4-panel-plugin-screenshooter 
License:        GPLv2+
Summary:        Screenshot Plugin for the Xfce Panel
Group:          System/GUI/XFCE 
Requires:       SFExfce4-panel
Requires:       SFExfce4-screenshooter 

%description -n xfce4-panel-plugin-screenshooter 
Xfce4 Screenshooter is a tool for taking screenshots, it can capture the entire screen, the active window or a selected region. Screenshots may be taken with a user-specified delay and the resulting images can be saved to a PNG file, copied it to the clipboard, opened with another application, or uploaded to ZimageZ, a free online image hosting service.   

This package contains the Xfce panel plugin. 

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi 

./configure --prefix=%{_prefix}         \
        --bindir=%{_bindir}             \
        --libdir=%{_libdir}             \
        --libexecdir=%{_libexecdir}     \
        --datadir=%{_datadir}           \
        --mandir=%{_mandir}             \
        --sysconfdir=%{_sysconfdir}	\
        --enable-xsltproc	        \
        --enable-xml2po 

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_bindir}/xfce4-screenshooter
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/xfce4-screenshooter.1* 
%{_datadir}/icons/hicolor/48x48/apps/applets-screenshooter.png 
%{_datadir}/icons/hicolor/scalable/apps/applets-screenshooter.svg 
%{_datadir}/applications/xfce4-screenshooter.desktop 

%files -n xfce4-panel-plugin-screenshooter 
%defattr(-,root,bin) 
%dir %{_libexecdir}/xfce4 
%dir %{_libexecdir}/xfce4/panel-plugins 
%{_libexecdir}/xfce4/panel-plugins/xfce4-screenshooter-plugin 
%{_datadir}/xfce4/panel-plugins/screenshooter.desktop 

%changelog
* Fri Jun 10 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec for Xfce4-screenshooter 
