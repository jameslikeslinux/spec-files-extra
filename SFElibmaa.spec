#
# spec file for package SFElibmaa
#
# includes module: libmaa
#

%include Solaris.inc
%define srcname libmaa

Name:		SFElibmaa
IPS_package_name:	library/libmaa
Group:		System/Libraries
Summary:	Library providing low-level data structures helpful for writing compilers
URL:		https://sourceforge.net/projects/dict/
Meta(info.upstream):	Aleksey Cheusov <vle@gmx.net>
Version:	1.3.1
License:	LGPLv2+
SUNW_Copyright:	libmaa.copyright
Source:		%sf_download/project/dict/%srcname/%srcname-%version/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc
BuildRequires:	compatibility/ucb

# Taken from doc/libmaa.tex in the distribution tarball
%description
The LIBMAA library provides many low-level data structures which are
helpful for writing compilers, including hash tables, sets, lists,
debugging support, and memory management.  Although LIBMAA was designed
and implemented as a foundation for the Khepera Transformation System,
the data structures are generally applicable to a wide range of
programming problems.

The memory management routines are especially helpful for improving the
performance of memory-intensive applications.

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

./configure --prefix=%_prefix

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
%_libdir/libmaa.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/maa.h


%changelog
* Sat Dec 17 2011 - Alex Viskovatoff
- Bump to 1.3.1
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sat Jun 11 2011 - Alex Viskovatoff
- Add missing build dependency
* Tue Jan 25 2011 - Alex Viskovatoff
- Initial spec
