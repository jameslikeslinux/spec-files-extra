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

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc 

Name:           midori
Version:        0.3.6
Release:        1
License:        LGPLv2.1
Summary:        Lightweight Webkit-based Web Browser
Url:            http://twotoasts.de/index.php?/pages/midori_summary.html
Group:          Productivity/Networking/Web/Browsers
Source:         http://archive.xfce.org/src/apps/%{name}/0.3/%{name}-%{version}.tar.bz2

# Requires at least WebKitGTK+ and Vala for Midori 0.4.x

Requires: 		SFEwebkitgtk

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Midori is a lightweight web browser based on WebKit and GTK+. Its major
features are:
 
* Tabs, windows and session management.
* Flexibly configurable Web Search.
* User scripts and user styles support.
* Straightforward bookmark management.
* Customizable and extensible interface.
* Extensions such as Adblock, form history, mouse gestures or cookie management.
 
%prep
%setup -q

%build
export CC=gcc
export CXX=g++
export PATH=/usr/g++/bin:$PATH:/usr/perl5/bin
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -D__C99FEATURES__"
export LDFLAGS="%_ldflags"
export PYTHON=/usr/bin/python

# --debug-level=debug is the default an partially overrides CFLAGS
# by specifiying --docdir the HTML help is installed into the right location
./waf configure \
    --nocache \
    --debug-level=none \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_localstatedir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_defaultdocdir}/%{name} \
    --enable-addons \
    --disable-vala

./waf build -v --nocache %{?_smp_mflags}
 
%install
./waf install --nocache --destdir=%{buildroot}
 
#install -D -p -m 644 HACKING TODO TRANSLATE \
#    %{buildroot}%{_defaultdocdir}/%{name}
 
#%update_desktop_file -i %{name}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif
 
#%clean
#rm -rf %{buildroot}
%clean
rm -rf $RPM_BUILD_ROOt 
%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

 
%files
%defattr(0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/%{name}
%dir %{_libdir}/midori
%{_libdir}/midori/*.so
%dir %attr (0755, root, bin) %{_sysconfdir}
%config(noreplace) %{_sysconfdir}/xdg/midori
#%config(noreplace) %{_sysconfdir}/xdg/midori/search
%{_datadir}/%{name}/
%{_datadir}/doc/midori/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/status/news-feed.*
%{_datadir}/icons/hicolor/*/categories/extension.*
%{_datadir}/icons/hicolor/scalable/apps/midori.*
%{_datadir}/icons/hicolor/*/apps/midori.png

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif 
 
%changelog
* Tue Jul 12 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec 
