#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name tumbler
%define src_url http://archive.xfce.org/src/xfce/%{src_name}/0.1/
 
Name:           SFEtumbler
Summary:        Thumbnail management for Xfce
Version:        0.1.22
URL:            http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
License:	LGPLv2+
Patch1:		tumbler-01-sunstudio.diff
SUNW_Copyright:	tumbler.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires: 	SUNWdbus
BuildRequires:	SUNWgtk-doc
BuildRequires:	SUNWgnome-xml-share
Requires:	%{name}-root
 
%description
Tumbler is a D-Bus service for applications to request thumbnails for
various URI schemes and MIME types. It is an implementation of the
thumbnail management D-Bus specification described on http://live.gnome.org/ThumbnailerSpec
 
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%package devel
Summary:	%{summary} - developer files
Group:		system/gui/xfce
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

export PATH=/usr/gnu/bin:$PATH

./configure --prefix=%{_prefix}		\
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
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/*.so.*
%{_libdir}/tumbler-1
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_datadir}/dbus-1/services/*.service
 
%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%dir %{_datadir}/gtk-doc/html/tumbler
%doc %{_datadir}/gtk-doc/html/tumbler/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif
 
%changelog
* Sat Sep 24 2011 - Ken Mays <kmays2000@gmail.com>
- Backed to 0.1.22
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Wed Apr 13 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec
