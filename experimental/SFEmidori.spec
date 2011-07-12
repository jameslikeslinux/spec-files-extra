#
# spec file for package SFEmidori
# by Ken Mays
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
 
# Please submit bugfixes or comments via http://sourceforge.net/projects/pkgbuild/support
#
 
 
 
Name:           midori
Version:        0.3.6
Release:        1
License:        LGPLv2.1
Summary:        Lightweight Webkit-based Web Browser
Url:            http://twotoasts.de/index.php?/pages/midori_summary.html
Group:          Productivity/Networking/Web/Browsers
Source:         http://archive.xfce.org/src/apps/%{name}/0.3/%{name}-%{version}.tar.bz2
BuildRequires:  developer/gnome/gnome-doc-utils
BuildRequires:  developer/documentation-tool/gtk-doc
BuildRequires:  developer/gnome/gettext
BuildRequires:  library/desktop/gtk2
BuildRequires:  library/libidn
BuildRequires:  library/libnotify
BuildRequires:  library/libsoup
BuildRequires:  library/libxml
# Update to at least SQLite 3.7.7.1 (get older one from kde4sol-dev) 
# http://solaris.bionicmutton.org/pkg/4.6.0//en/index.shtml
BuildRequires:  sqlite
BuildRequires:  library/libunique
BuildRequires:  runtime/python-26
# Requires at least WebKitGTK+ and Vala 0.13.1
BuildRequires:  webkit

# for rsvg-convert utility
BuildRequires:  rsvg-view
BuildRequires:  update-desktop-files
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# for valac
BuildRequires:  vala
Recommends:     %{name}-lang = %{version}
Recommends:     xdg-utils
 
%description
Midori is a lightweight web browser based on WebKit and GTK+. Its major
features are:
 
* Tabs, windows and session management.
* Flexibly configurable Web Search.
* User scripts and user styles support.
* Straightforward bookmark management.
* Customizable and extensible interface.
* Extensions such as Adblock, form history, mouse gestures or cookie management.
 
%package devel
License:        LGPLv2.1
Summary:        Development Files for Midori
Group:          Development/Libraries/C and C++
Recommends:     vala
 
%description devel
This package contains development files needed to develop extensions for
Midori.
 
 
%lang_package
%prep
%setup -q
 
%build
export CFLAGS="%{optflags}"
# --debug-level=debug is the default an partially overrides CFLAGS
# by specifiying --docdir the HTML help is installed into the right location
./waf configure \
    --nocache \
    --enable-apidocs \
    --debug-level=none \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_localstatedir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_defaultdocdir}/%{name}
./waf build -v --nocache %{?_smp_mflags}
 
%install
./waf install --nocache --destdir=%{buildroot}
 
install -D -p -m 644 HACKING TODO TRANSLATE \
    %{buildroot}%{_defaultdocdir}/%{name}
# API doc needs to be installed manually
install -d -m 755 %{buildroot}%{_datadir}/gtk-doc/html/%{name}
install -D -p -m 644 _build_/docs/api/midori/html/* \
    %{buildroot}%{_datadir}/gtk-doc/html/%{name}
 
#%update_desktop_file -i %{name}
 
# fix lang: no -> nb
mv %{buildroot}%{_datadir}/locale/{no,nb}
rm -rf %{buildroot}%{_datadir}/locale/{ast,kk,tl_PH,ur_PK}
%find_lang %{name}
 
%clean
rm -rf %{buildroot}
 
%post
%desktop_database_post
%icon_theme_cache_post
 
%postun
%desktop_database_postun
%icon_theme_cache_postun
 
%files
%defattr(0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%doc %{_defaultdocdir}/%{name}
%{_bindir}/%{name}
%dir %{_libdir}/midori
%{_libdir}/midori/*.so
%dir %{_sysconfdir}/xdg/midori
%dir %{_sysconfdir}/xdg/midori/extensions
%dir %{_sysconfdir}/xdg/midori/extensions/libadblock.so
%config(noreplace) %{_sysconfdir}/xdg/midori/search
%config(noreplace) %{_sysconfdir}/xdg/midori/extensions/libadblock.so/config
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/status/news-feed.*
%{_datadir}/icons/hicolor/*/categories/extension.*
%{_datadir}/icons/hicolor/*/apps/%{name}.*
 
%files devel
%defattr(0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/midori-0.3
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/history-list.*
 
%files lang -f %{name}.lang
 
%changelog
* Tue Jul 12 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec 
