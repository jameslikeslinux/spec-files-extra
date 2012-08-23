#
# spec libedit for package file
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%define tarball_version	20120601-3.0
%define tarball_name	libedit

Name:		SFEeditline
Summary:	A command line editing and history library
Version:	3.0
License:	BSD
Url:		http://www.thrysoee.dk/editline/
Source:		http://www.thrysoee.dk/editline/%{tarball_name}-%{tarball_version}.tar.gz
Patch1:		libedit-01-termcap.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{tarball_name}-%{tarball_version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure	\
	--prefix=%{_prefix}	\
	--sysconfdir=%{_sysconfdir}	\
	--libdir=%{_libdir}	\
	--bindir=%{_bindir}	\
	--includedir=%{_includedir}	\
	--mandir=%{_mandir}	\
	--disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Jun 02 2012 - Milan Jurik
- better multiarch support
* Sun Jul 31 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- omit -fast option.
* Sun Jun  5 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Fix dependency using pnm.
* Sat Mar 26 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Change permissions.
* Tue Jan  5 JST 2010 TAKI, Yasushi <taki@justplayer.com>
- Initial Revision
