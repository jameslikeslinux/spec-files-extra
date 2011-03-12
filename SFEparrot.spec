#
# spec file for package SFEparrot
#
# includes module: parrot
#

%include Solaris.inc
%define srcname parrot

Name:		SFE%srcname
Summary:	Register-based virtual machine designed to run dynamic languages efficiently
URL:		http://www.parrot.org/
Vendor:		Parrot Foundation
Version:	3.0.0
License:	Artistic License 2.0
Source:		ftp://ftp.parrot.org/pub/%srcname/releases/supported/%version/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

# Don't require perl-5 explicitly, since all Solaris systems have it,
# and we don't want to require a specific minor version.
#BuildRequires:	SUNWperl584core
#Requires:	SUNWperl584core

%package devel
Summary:	%summary - development files
SUNW_BaseDir:	%_basedir
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

perl Configure.pl --prefix=%_prefix --cc=cc --cxx=CC --optimize
gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%_prefix
rm lib/*.a
mv src share

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir
%_libdir/libparrot.so
%_libdir/%srcname
%dir %attr (-, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%srcname
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_docdir
%_docdir/%srcname

%files devel
%defattr (-, root, bin)
%_includedir/%srcname/%version
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, sys) %_datadir/src
%_datadir/src/%srcname/%version


%changelog
* Fri Mar 11 2011 - Alex Viskovatoff
- Initial spec
