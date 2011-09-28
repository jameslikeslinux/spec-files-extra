#
# spec file for package SFEgmpc
#
# use gcc to compile
# works: snv104 / pkgbuild 1.3.91
# works: snv104 / pkgbuild 1.2.0
# works: snv96  / pkgbuild 1.3.1


%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname gmpc

# This package no longer exists
#%define SFEgtkmm   %(/usr/bin/pkginfo -q SFEgtkmm && echo 1 || echo 0)
%define SFEgtkmm 0

Name:                    SFEgmpc
Summary:                 Gnome Music Player Daemon client
URL:                     http://sarine.nl/gmpc/
Version:                 0.20.0
License:                 GPLv2+
SUNW_Copyright:          gmpc.copyright
Source:                  http://download.sarine.nl/Programs/%srcname/%{version}/%srcname-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:		 SFEgob
BuildRequires:		 developer/vala
BuildRequires:		 library/perl-5/xml-parser
Requires:		 library/perl-5/xml-parser
BuildRequires:		 SFElibmpd-devel
#test#BuildRequires:           SFEavahi-devel
Requires:		SFElibmpd
Requires:		SUNWzlib

%if %SFEgtkmm
BuildRequires:		SFEgtkmm-devel
Requires:		SFEgtkmm
%else
BuildRequires:		SUNWgtkmm-devel
Requires:		SUNWgtkmm
%endif

#test#Requires:		       SFEavahi
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export LDFLAGS="%_ldflags -lxnet -lz"

export CC=gcc
export CXX=g++
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif

CC=$CC CXX=$CXX CFLAGS="$CFLAGS" XGETTEXT=/bin/gxgettext MSGFMT=/bin/gmsgfmt \
./configure --prefix=%_prefix
gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
#in case old pkgbuild does not automatically place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}

%if %{build_l10n}
%else
rm -rf $RPM_BUILD_ROOT/%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%doc README ChangeLog COPYING NEWS AUTHORS TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gmpc
%{_datadir}/gmpc/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%_mandir

%dir %attr (-, root, other) %_datadir/icons
%_datadir/icons/Humanity
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/scalable
%dir %attr (-, root, other) %_datadir/icons/hicolor/scalable/apps
%_datadir/icons/hicolor/scalable/apps/%srcname.svg
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%_datadir/icons/hicolor/16x16/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22/apps
%_datadir/icons/hicolor/22x22/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48
%dir %attr (-, root, other) %_datadir/icons/hicolor/48x48/apps
%_datadir/icons/hicolor/48x48/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64/apps
%_datadir/icons/hicolor/64x64/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/72x72
%dir %attr (-, root, other) %_datadir/icons/hicolor/72x72/apps
%_datadir/icons/hicolor/72x72/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/96x96
%dir %attr (-, root, other) %_datadir/icons/hicolor/96x96/apps
%_datadir/icons/hicolor/96x96/apps/%srcname.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128/apps
%_datadir/icons/hicolor/128x128/apps/%srcname.png



%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Mon Aug 19 2011 - Alex Viskovatoff
- Conform to the SFE practice of letting the environment choose the gcc
* Thu Aug 11 2011 - Alex Viskovatoff
- Fix directory attributes
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Tue Apr 12 2011 - Alex Viskovatoff
- Add missing build dependencies
* Wed Oct  6 2010 - Alex Viskovatoff
- Bump to version 0.20.0; use gmake
- Fix icon and man packaging
- Add Requires SUNWlibz; add -lz to LDFLAGS
* Sun Dec 27 2009 - Thomas Wagner
- remove SFEcurl|SUNWcurl - no longer used by gmpc
* Mon Dec 22 2008 - Thomas Wagner
- add nice and clean conditional (Build-)Requires: %if %SUNWgtkmm ... %else ... SFEgtkmm(-devel)
- create %{_docdir} in case old pkgbuild does not
* Sat Dec 20 2008 - Thomas Wagner
- adjust download URL
- add nice and clean conditional (Build-)Requires: %if %SUNWcurl ... %else ... SFEcurl(-devel)
- add LDFLAGS for network libs
- reduce files in %doc, add permissions to %{_docdir}
* Thu Jan 03 2008 - Thomas Wagner
- enabled building in parallel
* Sun Dec 02 2007 - Thomas Wagner
- bump to 0.15.5.0, add version_sub (currently at "0")
- remove --disable-sm (Session Manager)
- switch to new location of SFEcurl --with-curl=/usr/gnu
* Wed Nov 28 2007 - Thomas Wagner
- remove (Build-)Requires: SFEavahi(-devel) - needs more love (change to SUNW... bonjour/avahi/zeroconf)
- change removal of "/locale" if !build_l10n to be rm -rf (diry not longer empty)
* Tue Sep 04 2007  - Thomas Wagner
- bump to 0.15.1, add %{version} to Download-Dir (might change again)
- conditional !%build_l10n rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
- pause avahi/zeroconf on client side (will be re-enabled later)
* Sat May 26 2007  - Thomas Wagner
- bump to 0.15.0
- set compiler to gcc
- builds with Avahi, if present
* Thu Apr 06 2007  - Thomas Wagner
- Initial spec
