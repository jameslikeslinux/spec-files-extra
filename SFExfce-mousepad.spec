#
# spec file for package XFCE mousepad 0.2.16
#
# by Ken Mays

%include Solaris.inc

%define src_name mousepad
%define src_url http://archive.xfce.org/src/apps/mousepad/0.2/

Name:           SFExfce-mousepad
Summary:        Simple Xfce-oriented Text Editor
Version:        0.2.16
URL:            http://www.xfce.org/
Source:         %{src_url}/%{src_name}-%{version}.tar.bz2
Group:          User Interface/Desktops
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Patch1:         mousepad-01-find-and-replace.diff
Patch2:         mousepad-02-desktop.diff
BuildRequires:  SFElibxfcegui4 
Recommends:     %{name}-lang = %{version}
 
%description
Mousepad is a simple text editor for Xfce which has the following features:
* Complete support for UTF-8 text
* Cut/Copy/Paste and Select All text
* Search and Replace
* Font selection
* Word Wrap
* Character coding selection
* Auto character coding detection (UTF-8 and some codesets)
* Manual codeset setting
* Infinite Undo/Redo by word
* Auto Indent
* Multi-line Indent
* Display line numbers
* Drag and Drop
* Printing

%lang
 
%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

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
%{_bindir}/mousepad
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
 
%files lang -f %{name}.lang
 
%changelog
* Wed Jun 8 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec for Xfce mousepad 0.2.16
