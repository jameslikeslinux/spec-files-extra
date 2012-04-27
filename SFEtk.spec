#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define _basedir /usr/gnu

Name:                SFEtk
IPS_Package_Name:    runtime/tk-85
Summary:             Tk - TCL GUI Toolkit
Version:             8.5.11
Source:              %{sf_download}/tcl/tk%{version}-src.tar.gz
SUNW_Copyright:      %{name}.copyright

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr
Requires: SUNWlibms
Requires: SUNWxwplt
Requires: SUNWxwrtl
Requires: SFEtcl

%package devel
Summary: %{summary} - development files
SUNW_BaseDir:        %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n tk%version/unix

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
	    --enable-shared \
	    --enable-threads

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/tkConfig.sh
%{_libdir}/libtk*
%dir %attr (0755, root, bin) %{_libdir}/tk8.5
%{_libdir}/tk8.5/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%dir %attr (0755, root, bin) %{_mandir}/mann
%{_mandir}/man1/*
%{_mandir}/mann/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Thu Apr 26 2012 - Logan Bruns <logan@gedanken.org>
- Bump to 8.5.11. 
- Set IPS name to tk-85 and moved to /usr/gnu to avoid conflict with OS provided package. 
- Switched to gcc to avoid needing to pull in sunmath which can cause
  problems for gcc compiled packages linking against IPS.
- Added copyright file.
* Sat Sep 29 2007 - dick@nagual.nl
- Bumped to version 8.4.16
* Wed Jul 11 2007 - dick@nagual.nl
- Bumped to version 8.4.15
* Sun Jun 03 2007 - dick@nagual.nl
- Corrected the location of the mann directory
* Mon May 28 2007 - dick@nagual.nl
- Initial spec
