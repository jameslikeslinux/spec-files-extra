#
# spec file for package XFCE ristretto 
#
# by Ken Mays

%include Solaris.inc

%define src_name ristretto
%define src_url http://archive.xfce.org/src/apps/ristretto/0.2/

Name:           SFExfce4-ristretto
Summary:        Image Viewer
Version:        0.2.3
URL:            http://www.xfce.org/
Source:         %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SFElibxfcegui4 
BuildRequires:  SUNWlibexif
BuildRequires:  SFElibxfce4ui
BuildRequires:  SFEthunar
BuildRequires:  SFExfce4-dev-tools 
 
%description
Ristretto is a simple image viewer for Xfce

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
%{_bindir}/ristretto 
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/applications/ristretto.desktop 
%{_datadir}/icons/hicolor/*/apps/ristretto.* 
%{_datadir}/doc 
%{_datadir}/locale

%changelog
* Tue Jan 17 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 0.2.3
* Fri Oct 7 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 0.1.0
* Tue Oct 5 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec (0.0.93) 
