#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name thunar-vfs
%define src_url http://archive.xfce.org/xfce/4.8/src/

Name:		SFEthunar-vfs
Summary:	Thunar VFS
Version:	1.2.0
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		thunar-vfs-plugin-01-freespace.diff
Group:		User Interface/Desktops
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:	SFExfce4-dev-tools
BuildRequires:	SFElibxfcegui4-devel
Requires:	SFElibxfcegui4
BuildRequires:	SFElibxfce4ui-devel
Requires:	SFElibxfce4ui
Requires:	SFExfconf
BuildRequires:	SFEthunar-devel
Requires:	SFEthunar
BuildRequires:	SUNWgtk-doc
BuildRequires:	SUNWgnome-xml-share

%package devel
Summary:	%{summary} - developer files
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	--bindir=%{_bindir}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-gtk-doc		\
	--disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

# delete libtool .la files
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_libdir}/*thunar*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_datadir}/thumbnailers

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Oct 8 2011 - Ken Mays <kmays2000@gmail.com>
- Added patch for disk avail space calculation bug
* Sat Mar 26 2011 - Milan Jurik
- Initial version
