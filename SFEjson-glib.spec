#
# Copyright (c) 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


%include Solaris.inc

Name:		SFEjson-glib
IPS_Package_Name:	library/desktop/json-glib
Summary:	JSON parser library for GLib
Version:	0.12.6
License:	LGPL v2.1
Group:		Desktop (GNOME)/Libraries
Source:		http://ftp.gnome.org/pub/GNOME/sources/json-glib/0.12/json-glib-%{version}.tar.bz2
Url:		http://live.gnome.org/JsonGlib
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgtk-doc
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-base-libs

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel

%prep
%setup -q -n json-glib-%version

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
            --includedir=%{_includedir}	\
	    --mandir=%{_mandir}		\
	    --enable-gtk-doc		\
	    --disable-static

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc AUTHORS COPYING ChangeLog NEWS README
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
#%{_libdir}/girepository-1.0
%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/gir-1.0
%dir %attr (0755, root, other) %{_docdir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Sun Dec 11 2011 - Milan Jurik
- bump to 0.12.6
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
