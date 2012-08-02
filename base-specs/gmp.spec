#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#

##TODO## think on usr-gnu.inc define infodir inside /usr/gnu/share to avoid conflicts
%define _infodir           %{_datadir}/info

Name:		gmp
Version:	5.0.5
Source:		http://ftp.sunet.se/pub/gnu/gmp/gmp-%{version}.tar.bz2
Patch1:		gmp-01-solaris.diff
Patch2:		gmp-02-extern-inline-gmp-h.in.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags -L/usr/gnu/lib -R/usr/gnu/lib"
export CXXFLAGS="%cxx_optflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export ABI=64
else
        export ABI=32
fi

./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --infodir=%{_infodir}	\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --disable-cxx               \
	    --enable-fat

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue May 29 2012 - Milan Jurik
- bump to 5.0.5
* Fri Mar 9 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 5.0.4
- Fixed SIMD detection on legacy x86 computers
* Mon Oct 10 2011 - Milan Jurik
- go with proper multiarch
