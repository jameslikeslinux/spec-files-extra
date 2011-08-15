#
# spec file for package SFElibmpdclient
#
# includes module: libmpdclient
#

%include Solaris.inc
%define srcname libmpdclient

Name:		SFElibmpdclient
Summary:	Asynchronous API library for interfacing to MPD
URL:		http://mpd.wikia.com/wiki/ClientLib:libmpdclient
Meta(info.upstream):	Max Kellermann <max@duempel.org>
Version:	2.4
License:	BSD
SUNW_Copyright:	libmpdclient.copyright
Source:		%sf_download/project/musicpd/%srcname/%version/%srcname-%version.tar.bz2
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc


%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name


%prep
%setup -q -n %srcname-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

# --disable-static doesn't do what it's supposed to, but use it anyway
./configure --prefix=%_prefix --disable-static

# Be modern and use libxnet instead of libsocket
sed 's/-lsocket -lnsl/-lxnet/' Makefile > Makefile.xnet
mv Makefile.xnet Makefile

gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_libdir/*.la

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_libdir
%_libdir/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %attr (0755, root, other) %_includedir/mpd
%_includedir/mpd/*
%dir %attr (0755, root, other) %_libdir/pkgconfig 
%_libdir/pkgconfig/%srcname.pc
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/*


%changelog
* Thu Jul 21 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Tue Jan 18 2011 - Alex Viskovatoff
- Initial spec
