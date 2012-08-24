#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name garcon
%define src_url http://archive.xfce.org/src/xfce/%{src_name}/0.1/

Name:		SFEgarcon
IPS_Package_Name:	library/desktop/garcon
Version:	0.1.12
Summary:	Implementation of the freedesktop.org menu specification
License:	LGPLv2+ and GFDLv1.1
SUNW_Copyright:	garcon.copyright
Group:          Desktop (GNOME)/Libraries
URL:		http://xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:	SUNWgtk-doc
BuildRequires:	SUNWgnome-xml-share
Requires:	%{name}-root

%description
Garcon is an implementation of the freedesktop.org menu specification replacing
the former Xfce menu library libxfce4menu. It is based on GLib/GIO only and 
aims at covering the entire specification except for legacy menus.

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%package devel
Summary:	%{summary} - developer files
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

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
# GNU xgettext needed
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
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/desktop-directories

%files root
%defattr(-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/menus
%config(noreplace) %{_sysconfdir}/xdg/menus/xfce-applications.menu

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Aug 23 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 0.1.12
* Wed Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 0.1.9
* Tue Aug 23 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 0.1.8
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thu Aug 21 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 0.1.7
* Mon Mar 21 2011 - kmays2000@gmail.com
- Bump to 0.1.6
* Mon Mar 21 2011 - Milan Jurik
- initial spec
