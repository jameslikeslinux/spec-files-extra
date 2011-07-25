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
Meta(info.upstream):	Parrot Developers <parrot-dev@lists.parrot.org>
Version:	3.3.0
License:	Artistic 2.0
SUNW_Copyright:	
Source:		ftp://ftp.parrot.org/pub/%srcname/releases/supported/%version/%srcname-%version.tar.bz2
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
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sat Apr 23 2011 - Alex Viskovatoff
- Bump to 3.3.0
* Fri Mar 11 2011 - Alex Viskovatoff
- Initial spec
