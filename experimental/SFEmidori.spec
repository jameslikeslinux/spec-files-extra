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
%define srcname midori

Name:           SFEmidori
Version:        0.3.6
Release:        1
License:        LGPLv2.1
SUNW_copyright: midori.copyright
Summary:        Lightweight Webkit-based Web Browser
Url:            http://twotoasts.de/index.php?/pages/midori_summary.html
Meta(info.upstream): Christian Dywan <christian@twotoasts.de>
Group:          Applications/Internet
Source:         http://archive.xfce.org/src/apps/%srcname/0.3/%srcname-%version.tar.bz2

# Requires at least WebKitGTK+ and Vala for Midori 0.4.x

Requires: 		SFEwebkitgtk

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-build

%description
Midori is a lightweight web browser based on WebKit and GTK+. Its major
features are:
 
* Tabs, windows and session management.
* Flexibly configurable Web Search.
* User scripts and user styles support.
* Straightforward bookmark management.
* Customizable and extensible interface.
* Extensions such as Adblock, form history, mouse gestures or cookie management.
 
%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%prep
%setup -q -n %srcname-%version

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
    --docdir=%{_docdir}/%{srcname} \
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
 
%clean
rm -rf %buildroot
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
%{_bindir}/%{srcname}
%dir %{_libdir}/midori
%{_libdir}/midori/*.so
%dir %attr (0755, root, sys) %_sysconfdir
%dir %attr (0755, root, sys) %_sysconfdir/xdg
%config(noreplace) %{_sysconfdir}/xdg/midori
#%config(noreplace) %{_sysconfdir}/xdg/midori/search
%{_datadir}/%{srcname}/
%{_datadir}/doc/midori/*
%{_datadir}/applications/%{srcname}.desktop
%defattr(0755, root, other)
%dir %attr (0755, root, sys) %_prefix
%dir %attr (0755, root, bin) %_libdir
%dir %attr (0755, root, sys) %_datadir
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
* Sun Oct  1 2011 - Alex Viskovatoff
- Fix packaging; add SUNW_copyright
- Midori runs but is broken, displaying wierd characters instead of "://"
  in the URL field
* Tue Jul 12 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec 
