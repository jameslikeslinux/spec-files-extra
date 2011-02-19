#
# spec file for packages SFEtelepathy-gabble
#
# includes module(s): telepathy-gabble
#
# Owner:jefftsai
#
%include Solaris.inc

%include base.inc
%use telepathy_gabble = telepathy-gabble.spec

Name:                    SFEtelepathy-gabble
Summary:                 A Jabber/XMPP connection manager
Version:                 %{telepathy_gabble.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEtelepathy-glib
BuildRequires: SFEtelepathy-glib-devel
Requires: SFElibnice
BuildRequires: SFElibnice-devel
Requires: SFEcyrus-sasl
BuildRequires: SFEcyrus-sasl
BuildRequires: SUNWgtk-doc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version

mkdir -p %name-%version/%base_arch
%telepathy_gabble.prep -d %name-%version/%base_arch

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%telepathy_gabble.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%telepathy_gabble.install -d %name-%version/%base_arch

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch}/telepathy-gabble-%{telepathy_gabble.version} COPYING NEWS ChangeLog AUTHORS README
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}

%{_libdir}/telepathy-gabble
%{_libdir}/telepathy/gabble-0/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/man/*
%{_datadir}/doc/telepathy-gabble/*
%{_datadir}/dbus-1/*
%{_datadir}/telepathy/*

%changelog
* Sun Feb 13 2011 - Milan Jurik
- disable multiarch build
* Oct 12 2010 - jeff.cai@oracle.com
- created
