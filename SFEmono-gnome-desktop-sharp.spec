#
# spec file for package SFEmono-gnome-desktop-sharp
#
# includes module(s): gnome-desktop-sharp
#
%include Solaris.inc

Name:         SFEmono-gnome-desktop-sharp
License:      Other
Group:        System/Libraries
Version:      2.24.0
Summary:      gtk# - .NET bindings for the GNOME platform libraries
Source:       http://go-mono.com/sources/gnome-desktop-sharp2/gnome-desktop-sharp-%{version}.tar.bz2
Patch1:       gnome-desktop-sharp-01-Wall.diff
URL:          http://www.mono-project.org/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

BuildRequires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SFEmono-devel
BuildRequires: SFEmono-gtk-sharp
Requires: SFEmono-gtk-sharp
BuildRequires: SFEmono-gnome-sharp
Requires: SFEmono-gnome-sharp
Requires: SUNWgnome-base-libs
Requires: SUNWevolution-libs
Requires: SFEmono

%prep
%setup -q -n gnome-desktop-sharp-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export MONO_LIBS=/usr/mono:/usr/lib/mono

#autoconf
aclocal-1.10
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %dir %{_libdir}/mono
#%{_libdir}/mono/*
%{_libdir}/mono/gac
%{_libdir}/mono/gnomedesktop-sharp-2.20
%{_libdir}/mono/vte-sharp-0.16
%{_libdir}/mono/gnome-panel-sharp-2.24
%{_libdir}/mono/gtksourceview2-sharp-2.0
%{_libdir}/mono/wnck-sharp-2.20
%{_libdir}/mono/gnome-print-sharp-2.18
%{_libdir}/mono/rsvg2-sharp-2.0
#%dir %attr (0755, root, bin) %dir %{_libdir}/mono/gac
#%{_libdir}/mono/gac/*
#%dir %attr (0755, root, bin) %dir %{_libdir}/mono/gac/vte-sharp
#%{_libdir}/mono/gac/vte-sharp/*
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gnome-panel-sharp
%{_datadir}/gnomedesktop-sharp
%{_datadir}/rsvg2-sharp
%{_datadir}/wnck-sharp
%{_datadir}/gnome-print-sharp
%{_datadir}/gtksourceview2-sharp
%{_datadir}/vte-sharp

%changelog
* Fri Sep 16 2011 - jchoi4@pha.jhu.edu
- Initial spec
