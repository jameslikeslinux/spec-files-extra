#
# spec file for package XFCE gigolo
#
# by Ken Mays
#
# Note: Thunar VFS dependency 
 
%include Solaris.inc

%define src_name gigolo
%define src_url http://archive.xfce.org/src/apps/gigolo/0.4

Name:           SFExfce-gigolo
Summary:        Frontend to easily manage connections to remote filesystems
Version:        0.4.1
URL:            http://www.xfce.org/
Source:         %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SFElibxfcegui4 
BuildRequires:  SFEthunar-vfs
BuildRequires:  SFEthunar

 
%description
Gigolo is a frontend to easily manage connections to remote filesystems using
GIO/GVFS. It allows you to quickly connect/mount a remote filesystem and manage
bookmarks of such.


 
%prep
%setup -q -n %{src_name}-%{version}
#%patch1 -p1
#%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi 

sh autogen.sh
./waf configure --prefix=%{_prefix}         \
        --bindir=%{_bindir}             \
        --libdir=%{_libdir}             \
        --libexecdir=%{_libexecdir}     \
        --datadir=%{_datadir}           \
        --mandir=%{_mandir}             \
        --sysconfdir=%{_sysconfdir}

./waf build -v --nocache

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_bindir}/gigolo
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
 
 
%changelog
* Wed Jun 8 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec for Xfce gigolo
- WIP - Due to Thunar VFS - GIO/GVFS in Solaris pending issue
