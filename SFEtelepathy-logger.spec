#
# spec file for packages SFEtelepathy-logger
#
# includes module(s): telepathy-logger
#
# Owner:alfred
#
%include Solaris.inc

%use telepathy_logger = telepathy-logger.spec

Name:                    SFEtelepathy-logger
Summary:                 A connection manager based on libpurple for IM protocols.
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgtk3
BuildRequires: SUNWgtk3-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%telepathy_logger.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%telepathy_logger.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%telepathy_logger.install -d %name-%version

find $RPM_BUILD_ROOT%{_libdir} -name "*.la" -exec rm {} \;
find $RPM_BUILD_ROOT%{_libdir} -name "*.a" -exec rm {} \;

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/girepository-1.0/*
%{_libexecdir}/telepathy-logger
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1/*
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0
%{_datadir}/telepathy/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Jul 06 2011 - Brian Cameron <brian.cameron@oracle.com>
- created
