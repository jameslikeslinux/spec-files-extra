#
# spec file for package seed
#
# Copyright (c) 2010 Sun Microsystems, Inc.
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%define	src_name seed

Summary:	JavaScript interpreter
IPS_Package_Name:	runtime/javascript/seed
Name:		SFEseed
Version:	2.30.0
License:	LGPLv3
Group:		Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/seed/2.30/%{src_name}-%{version}.tar.bz2
Patch1:		seed-01-wall.diff
Patch2:		seed-02-gettext.diff
Patch3:		seed-03-util.diff
Patch4:         seed-04-seed.diff
Patch5:		seed-05-mpfr.diff
URL:		http://live.gnome.org/Seed
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:	SUNWdbus
Requires:	SFEgnome-js-common
Requires:	SFEgjs
Requires:	SUNWgtk2
Requires:	SFEwebkitgtk
Requires:	SUNWsqlite3-devel

%description
Seed is a library and interpreter, dynamically bridging (through
GObjectIntrospection) the WebKit JavaScriptCore engine, with the GNOME
platform. Seed serves as something which enables you to write
standalone applications in JavaScript, or easily enable your
application to be extensible in JavaScript.

%package devel
Summary:	Header files for seed library
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	SUNWglib2-devel
Requires:	SUNWgobject-introspection-devel
Requires:	SFEwebkitgtk-devel


%description devel
Header files for seed library.

%package apidocs
Summary:	seed library API documentation
Group:		Documentation
Requires:	SUNWgtk-doc

%description apidocs
API documentation for seed library.

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

intltoolize --copy --force --automake
libtoolize --force
aclocal 
autoheader
automake -a -c -f
autoconf

export CFLAGS="%{optflags} -I/usr/include/mpfr"
export CXXFLAGS="%{cxx_optflags} -I/usr/include/mpfr"

./configure --prefix=%{_prefix}		\
	--sysconfdir=%{_sysconfdir}	\
	--libexecdir=%{_libexecdir}	\
	--localstatedir=%{_localstatedir}	\
	--mandir=%{_mandir}	\
	--disable-static	\
	--enable-gtk-doc

make -j $CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

find %{buildroot} -name "*.a" -o -name "*.la" -exec rm {} \;

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_bindir}/seed
%{_libdir}/*.so*
%{_libdir}/seed
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/seed
%{_datadir}/seed
%{_datadir}/gtk-doc
%{_mandir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_includedir}

%changelog
* Tue Sep 08 2010 - yuntong.jin@sun.com
- Init spec
