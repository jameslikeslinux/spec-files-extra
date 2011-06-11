#
# spec file for package XFCE mousepad 0.2.16
#
# by Ken Mays

%include Solaris.inc

%define src_name xfmpc
%define src_url http://archive.xfce.org/src/apps/xfmpc/0.2/

Name:           SFExfce-xfmpc
Summary:        Simple Xfce-oriented Text Editor
Version:        0.2.1
URL:            http://www.xfce.org/
Source:         %{src_url}/%{src_name}-%{version}.tar.bz2
Group:          User Interface/Desktops
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SFElibmpd
BuildRequires:  SFElibxfce4ui 
BuildRequires:  SFElibxfce4util	
BuildRequires:  SUNWperl-xml-parser  
Suggests:       mpd

%description
Xfmpc is a lightweight Music Player Daemon (MPD) client application for the
Xfce desktop environment.

%lang
 
%prep
%setup -q -n %{src_name}-%{version}
sed -i 's:^Icon=stock_volume$:Icon=xfmpc:' xfmpc.desktop.in

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
        --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_bindir}/xfmpc
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
 
 
%changelog
* Wed Jun 8 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec for Xfce xfmpc 0.2.1
