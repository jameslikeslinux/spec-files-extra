#
# Copyright (c) 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%define pythonver 2.6

%include Solaris.inc

Name:                    SFEcaribou
Summary:                 Caribou On Screen Keyboard
Version:                 0.4.1
Source:			 http://ftp.gnome.org/pub/GNOME/sources/caribou/0.4/caribou-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgtk-doc
%endif
Requires: SUNWpygobject26
Requires: SUNWgtk3
Requires: SUNWclutter
BuildRequires: SUNWpygobject26-devel
BuildRequires: SUNWgtk3-devel
BuildRequires: SUNWclutter-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/xdg

%prep
%setup -q -n caribou-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir} \
            --includedir=%{_includedir}	\
            --sysconfdir=%{_sysconfdir}	\
	    --mandir=%{_mandir}		\
	    %{gtk_doc_option}		\
	    --disable-static

gmake -j $CPUS

%install
/bin/rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
/bin/rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/antler-keyboard
%{_libdir}/gtk-2.0
%{_libdir}/gtk-3.0
%{_libdir}/girepository-1.0
%{_libdir}/gnome-settings-daemon-3.0
%{_libdir}/python2.6/
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/antler
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/caribou
%{_datadir}/dbus-1
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Oct 23 2010 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 0.12.0.
* Wed Feb 03 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.10.0
* Sat Nov 14 2009 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.8.2
- Drop patch1
- Update source URL, add license
- Update dependencies
* Sun Jun 21 2009 - trisk@forkgnu.org
- Initial spec
