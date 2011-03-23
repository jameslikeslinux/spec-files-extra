#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name libxfce4ui
%define src_url http://archive.xfce.org/xfce/4.8/src/

Name:		SFElibxfce4ui
Summary: 	Widgets library for the Xfce desktop environment
Version: 	4.8.0
License:	LGPL
URL: 		http://www.xfce.org/
Source:         %{src_url}/%{src_name}-%{version}.tar.bz2
Group: 		Development/Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot: 	%{_tmppath}/%{name}-root
%include default-depend.inc
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:	SFExfce4-dev-tools
Requires:	SFElibxfce4util
BuildRequires:	SFElibxfce4util-devel
Requires	SFExfconf
BuildRequires:	SFExfconf-devel
Requires:	SUNWgnome-ui-designer
BuildRequires:	SUNWgnome-ui-designer-devel
BuildRequires:	SUNWgnome-xml-share
BuildRequires:	SUNWgtk-doc
Requires:	%{name}-root

%description
Widgets and other frequently used functions for the Xfce desktop environment.

%package devel
Summary:	%{summary} - developer files
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

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
./configure --prefix=%{_prefix}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-gtk-doc		\
	--disable-visibility		\
	--disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete libtool .la files
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/glade3
%dir %attr (0755, root, bin) %{_datadir}/glade3/catalogs
%{_datadir}/glade3/catalogs/*
%dir %attr (0755, root, bin) %{_datadir}/glade3/pixmaps
%{_datadir}/glade3/pixmaps/*
%dir %attr (0755, root, bin) %{_libdir}/glade3/modules
%{_libdir}/glade3/modules/*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Mar 21 2011 - Milan Jurik
- initial spec
