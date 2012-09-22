#
# spec file for package SFEconky
#
# includes module(s): conky
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

Name:                    SFEconky
IPS_Package_Name:	 desktop/system-monitor/conky
Summary:                 An advanced highly configurable system monitor for X  
Version:                 1.9.0
Source:                  %{sf_download}/conky/conky-%{version}.tar.gz
#Patch1:                  conky-1.9.0-opensolaris.diff
URL:                     http://conky.sourceforge.net/
License:                 GPLv3,BSD
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu
BuildRequires: SUNWgcc
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWlua
Requires:      SUNWlua

%prep
%setup -q -n conky-%version
#%patch1 -p1

export CFLAGS="%optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -lX11"

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CC=/usr/sfw/bin/gcc

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --x-includes=/usr/X11/include \
            --x-libraries=/usr/X11/lib
            --disable-mpd \ 
	    --disable-moc \
            --enable-weather-metar \
            --enable-lua-cairo

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/conky
%{_sysconfdir}/conky/*


%changelog
* Sat Sep 22 2012 - Ken Mays <kmays2000@gmail.com>
- Bumped to 1.9.0
* Sat Sep 22 2012 - Ken Mays <kmays2000@gmail.com>
- Bumped to 1.7.2
- Added patches/conky-1.7.2-opensolaris.diff
* Fri Apr  9 2010 - Miroslav Osladil <mira@osladil.cz>
- added dependency on SUNWgnome-common-devel
- use %{sf_download} in source url
* Tue Apr 06 2010 - Milan Jurik
- small cleanup
* Thu Apr 9 2009 - Alexander R. Eremin eremin@milax.org
- Initial spec file.
