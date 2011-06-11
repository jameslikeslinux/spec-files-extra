#
# spec file for package XFCE dict 
#
# by Ken Mays
#
# http://goodies.xfce.org/projects/applications/xfce4-dict

%include Solaris.inc

%define src_name xfce4-dict
%define src_url http://archive.xfce.org/src/apps/xfce4-dict/0.6/

Name:           SFExfce4-dict
Summary:        A client program to query different dictionaries
Version:        0.6.0
URL:            http://www.xfce.org/
Source:         %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:       SFElibxfcegui4 
Requires:       SFElibxfce4ui
Requires:       SFExfce4-panel
Requires:       SUNWperl-xml-parser
Suggests:       xfce4-panel-plugin-dict 
Requires:       SUNWpostrun


%description
Xfce4 Dictionary is written by Enrico Trger, and is a client program to query different dictionaries. It can query a Dict server (RFC 2229), open online dictionaries in a web browser or verify the spelling of a word using aspell or ispell. It contains a stand-alone application and a plugin for the Xfce panel. 

%package -n xfce4-panel-plugin-dict
License:        GPLv2+
Summary:        Dictionary Plugin for the Xfce Panel 
Group:          Productivity/Office/Dictionary 
Requires:       SFExfce4-panel
Requires:       SFExfce4-dict  

%description -n xfce4-panel-plugin-dict 
xfce4-dict allows you to search different kinds of dictionary services for words or phrases and shows you the result. Currently you can query a Dict server(RFC 2229), any online dictionary service by opening a web browser or search for words using the aspell/ispell program.   

This package contains the panel plugin for the Xfce panel. 

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
        --sysconfdir=%{_sysconfdir}     \
        --enable-gtk-doc                \
        --disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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
%{_bindir}/xfce4-dict
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/applications/*.desktop 
%{_datadir}/icons/hicolor/*/apps/* 
%{_mandir}/man1/xfce4-dict.1*   

%files -n xfce4-panel-plugin-dict 
%defattr(-,root,bin) 
%{_libexecdir}/xfce4/panel-plugins/xfce4-dict-plugin 
%{_datadir}/xfce4/panel-plugins/*.desktop
%files lang -f %{name}.lang 

%changelog
* Thu Jun 9 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec for Xfce dict 
