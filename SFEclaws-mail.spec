#
# spec file for package SUNWclaws-mail
#

%include Solaris.inc

%define SFEgnupg2	%(/usr/bin/pkginfo -q SFEgnupg2 && echo 1 || echo 0)

%define src_name         claws-mail

Name:                    SFEclaws-mail
Summary:                 Claws-Mail is an e-mail client (and news reader) based on GTK+
Version:                 3.7.9
License:                 GPLv3+
SUNW_Copyright:          claws-mail.copyright
Source:                  %{sf_download}/sylpheed-claws/%{src_name}-%{version}.tar.bz2
License:                 GPL
URL:                     http://claws-mail.org/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgsed
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWopenssl-include
BuildRequires: SFElibetpan-devel
Requires: SUNWlibmsr
Requires: SUNWgnome-base-libs
Requires: SUNWopenssl-libraries
%if %SFEgnupg2
Requires: SFEpth
Requires: SFElibassuan
Requires: SFEgnupg2
%else
Requires: SUNWpth
Requires: SUNWgnupg
%endif
Requires: SFEdillo
Requires: SFEbogofilter
Requires: SFElibetpan
BuildRequires: SUNWlibgpg-error-devel
Requires: SUNWlibgpg-error

%description
Claws-Mail is an e-mail client (and news reader) based on GTK+

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name
%endif


%prep
%setup -q -n %{src_name}-%{version}
/usr/gnu/bin/sed -i -e "s,CFLAGS -Wall -Wno-pointer-sign,CFLAGS,g" configure configure.ac
/usr/gnu/bin/sed -i -e "s,CFLAGS -std=gnu99 -DSOLARIS,CFLAGS -DSOLARIS,g" configure configure.ac
/usr/gnu/bin/sed -i -e "s,-Wno-deprecated-declarations,-errfmt=error," src/plugins/pgpcore/Makefile.am \
    src/plugins/pgpcore/Makefile.in \
    src/plugins/pgpinline/Makefile.am \
    src/plugins/pgpinline/Makefile.in \
    src/plugins/pgpmime/Makefile.am \
    src/plugins/pgpmime/Makefile.in
/usr/gnu/bin/sed -i -e "s,-Wno-deprecated-declarations,," src/plugins/smime/Makefile.in \
    src/plugins/smime/Makefile.am

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -xc99"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix}          \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared             \
            --disable-static            \
            --enable-ipv6		\
            --enable-jpilot		\
            --disable-trayicon-plugin 	\
            --disable-ldap              \
            --enable-spamassassin-plugin=yes

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
install -m 644 *.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
rm ${RPM_BUILD_ROOT}%{_bindir}/sylpheed-claws

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/%{src_name}
%{_libdir}/claws-mail/plugins/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/claws-mail.png
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/64x64
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/64x64/apps
%{_datadir}/icons/hicolor/64x64/apps/claws-mail.png
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/apps
%{_datadir}/icons/hicolor/128x128/apps/claws-mail.png
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/claws-mail

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/claws-mail.pc
%{_includedir}/claws-mail

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Apr 24 2011 - Milan Jurik
- minor cleanup
* Fri Apr 15 2011 - kmays2000@gmail.com
- Bumped to 3.7.9
- Detect ipv6, jpilot, spamassasin, gpgme
* Sun Jun 14 2010 - Milan Jurik
- use SUNW packages if possible
* Thu Jun 10 2010 - pradhap (at) gmail.com
- Bump to 3.7.6
- Fixed icons path
* Thu Oct 2 2008 - markwright@internode.on.net
- Detect aspell, disable pgp to avoid compiler error.
* Thu Oct 2 2008 - markwright@internode.on.net
- create
