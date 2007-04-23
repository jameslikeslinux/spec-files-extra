#
# spec file for package SFEwine.spec
#
# includes module(s): wine
#
%include Solaris.inc

%define src_name	wine
%define src_url		http://jaist.dl.sourceforge.net/sourceforge/%{src_name}

Name:                   SFEwine
Summary:                Windows Emulator
Version:                0.9.35
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			wine-01-nameconfict.diff
Patch2:			wine-02-configure.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWgnome-camera-devel
Requires:	SUNWgnome-camera
Requires:	SUNWhal
BuildRequires:	SUNWdbus-devel
Requires:	SUNWdbus
Requires:	SUNWxorg-clientlibs
BuildRequires:	SFEfontforge-devel
Requires:	SFEfontforge

%package devel
Summary:                 wine - developer files, /usr
SUNW_BaseDir:            %{_basedir}
Requires: %name
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
SFWLIB="-L/usr/SFW/lib -R/usr/SFW/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CC=/usr/sfw/bin/gcc
export CPPFLAGS="-I/usr/sfw/include -I/usr/X11/include -I/usr/gnu/include"
export CFLAGS="-O3 -fno-omit-frame-pointer -fpic -Dpic"
export LDFLAGS="-zignore $X11LIB $SFWLIB $GNULIB"
export LD_OPTIONS="-zignore"
export LD=/usr/ccs/bin/ld
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/wine
%defattr (-, root, other)
%{_datadir}/applications

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Mon Apr 23 2006 - dougs@truemail.co.th
- Fixed Summary
* Sun Apr 22 2006 - dougs@truemail.co.th
- Initial version
