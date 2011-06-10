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
BuildRequires:  SFElibxfcegui4 
BuildRequires:  SFElibxfce4ui
BuildRequires:  SFExfce4-panel
BuildRequires:  SUNWperl-xml-parser
Suggests:       xfce4-panel-plugin-dict 
 
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
        --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


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
