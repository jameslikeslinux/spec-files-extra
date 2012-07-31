#
# spec file for package: emerald
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): emerald
#

%include Solaris.inc

Name:		SFEemerald
Summary:      	Window decorator for compiz
Version:       	0.8.8
License:	GPLv2+
SUNW_Copyright:	emerald.copyright
Url: 		http://wiki.compiz.org/Decorators/Emerald
Source:	 	http://releases.compiz.org/0.8.8/emerald-0.8.8.tar.gz
Group:		Applications/Accessories
Distribution:   OpenSolaris
Vendor:		OpenSolaris Community
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   %{_basedir}
%include default-depend.inc

BuildRequires:  SUNWcompiz
Requires:  	SUNWcompiz
Requires:	SUNWgnome-base-libs
%if %option_with_gnu_iconv
Requires: 	SUNWgnu-libiconv
Requires: 	SUNWgnu-gettext
%else
Requires: 	SUNWuiu8
%endif

%description
The Emerald Window Decorator is a custom window decorator shipped with Compiz Fusion that allows for theming and full composite window decorations with the use of engines. Emerald allows for all sorts of different configurations and layouts of buttons, look, title bars and frames. Emerald Window Decorator is completely independent of any desktop, and you specify your own themes to use for it.

%prep
%setup -q -n emerald-%{version}

%build
./configure --prefix=%{_prefix}
#change strverscmp to strcmp in ./themer/main.c because it is deprecated
sed -i 's/strverscmp/strcmp/g' ./themer/main.c
sed 's/-Wall //' Makefile > Makefile.fixed
mv Makefile.fixed Makefile
#CFLAGS used to remove the zero size struct error.
make CFLAGS='-features=extensions'

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, bin) %{_libdir}/emerald
%{_libdir}/emerald/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/emerald
%{_datadir}/emerald/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/mimetypes/
%{_datadir}/icons/hicolor/48x48/mimetypes/*
%dir %attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, root) %{_datadir}/mime/packages
%{_datadir}/mime/packages/*
%dir %attr (0755, root, other) %{_datadir}/mime-info
%{_datadir}/mime-info/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr(0755, root, other) %{_datadir}/locale
%attr (-, root, other) %{_datadir}/locale/*

%changelog
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thu May 13 2010 - N.B.Prashanth <nbprash.mit@gmail.com>
- update to 0.8.8; use SUNWcompiz
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Add support for Indiana builds.
* Wed Nov 14 2007 - daymobrew@users.sourceforge.net
- Add l10n package.
* Thu Nov 01 2007 - trisk@acm.jhu.edu
- Fix file contents
- Remove -root
* Fri Sep 6 2007 - erwann@sun.com
- Initial spec

