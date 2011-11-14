#
# spec file for package SFEpcre-gpp
#
# includes module: pcre
#

%include Solaris.inc
%define srcname pcre
%define cc_is_gcc 1
%include base.inc
%define _prefix %_basedir/g++

Name:		SFEpcre-gpp
Summary:	Perl Compatible Regular Expressions (g++ built)
URL:		http://www.pcre.org/
Version:	8.12
#License:	LGPLv2+
#SUNW_Copyright:	pcre.copyright
Source:		ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%srcname-%version.tar.bz2
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

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%_prefix --enable-unicode-properties --disable-static --enable-pcregrep-libz --enable-pcregrep-libbz2

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
%_libdir/libpcre*.so*
%_bindir
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %dir %_docdir
%_docdir/%srcname
%_mandir/man1/*
%_mandir/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/*.h
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Aug 14 2011 - Alex Viskovatoff
- Initial spec
