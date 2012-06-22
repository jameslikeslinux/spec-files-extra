#
# spec file for package SFElibebml
#
# includes module(s): libebml
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define _prefix %_basedir/g++
%define srcname libebml

Name:		SFElibebml-gpp
IPS_package_name: library/g++/libebml
License:	LGPL
Summary:	Extensible Binary Meta Language
Group:		System Environment/Libraries
URL:		http://ebml.sourceforge.net
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	1.2.0
Source:		http://dl.matroska.org/downloads/%srcname/%srcname-%version.tar.bz2
Patch1:		libebml-01-makefile.diff
Patch2:		libebml-02-headers.diff
Patch3:		libebml-03-ebmlbinary.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWgmake
%if %(/usr/bin/pkginfo -q SFEcoreutils 2>/dev/null  && echo 1 || echo 0)
BuildRequires:	SFEcoreutils
%else
BuildRequires:	SUNWgnu-coreutils
%endif
BuildRequires:	SUNWloc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CXXFLAGS="%cxx_optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT=/usr/bin/msgfmt

cd make/linux
gmake -j$CPUS CXX=g++ AR=CC  DEBUGFLAGS=-g WARNINGFLAGS="" \
ARFLAGS="-xar -o" LOFLAGS=-fpic LIBSOFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -G -h "

%install
rm -rf $RPM_BUILD_ROOT
cd make/linux
gmake install_headers prefix=$RPM_BUILD_ROOT%{_prefix} INSTALL=ginstall
gmake install_sharedlib prefix=$RPM_BUILD_ROOT%{_prefix} INSTALL=ginstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri Jun 22 2012 - Logan Bruns <logan@gedanken.org>
- Accept either SFEcoreutils or SUNWgnu-coreutils for buildrequires.
* Fri Dec  2 2011 - Thomas Wagner 
- Add IPS package name
- copy SFElibebml.spec to SFElibebml-gpp.spec
- move to gcc/g++ and relocate to prefix /usr/g++
* Sat Feb  5 2011 - Alex Viskovatoff
- Update to 1.2.0, adding one patch
* Thu Jan 27 2011 - Alex Viskovatoff
- Go back to using -library=stdcxx4
* Tue Nov 23 2010 - Alex Viskovatoff
- Use stdcxx.inc instead of -library=stdcxx4; install in /usr/stdcxx
* Fri Oct  1 2010 - Alex Viskovatoff
- Update to 1.0.0; use stdcxx (requires Solaris Studio 12u1)
- Patch linux Makefile so that it works with Linux and Solaris
  instead of creating a new Makefile for Solaris.
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial version
