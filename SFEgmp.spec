#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use gmp_64 = gmp.spec
%endif

%include base.inc
%use gmp = gmp.spec

##TODO## think on usr-gnu.inc define infodir inside /usr/gnu/share to avoid conflicts
%define _infodir           %{_datadir}/info


Name:		SFEgmp
IPS_Package_Name:	sfe/library/gmp
Summary:	GNU Multiple Precision Arithmetic Library
Group:		Development/Libraries
Version:	%{gmp.version}
License:	GPLv3+
SUNW_Copyright:	gmp.copyright
URL:		http://gmplib.org/
SUNW_BaseDir:	%{_basedir}/%{_subdir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibm
Requires: SUNWlibm

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}/%{_subdir}
Requires: %name

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%gmp_64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%gmp.prep -d %name-%version/%base_arch


%build
%ifarch amd64 sparcv9
%gmp_64.build -d %name-%version/%_arch64
%endif

%gmp.build -d %name-%version/%{base_arch}


%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%gmp_64.install -d %name-%version/%_arch64
%endif

%gmp.install -d %name-%version/%{base_arch}

%clean
rm -rf %{buildroot}

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmp.info gmp.info-1 gmp.info-2' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmp.info gmp.info-1 gmp.info-2' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Mar 9 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 5.0.4
- Fixed SIMD detection on legacy x86 computers
* Sat Jan  7 2012 - Thomas Wagner
- add (Build)Requires: SUNWlibm
* Mon Oct 10 2011 - Milan Jurik
- bump to 5.0.2, go with proper multiarch
- add IPS package name with sfe prefix to avoid collision
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jun  6 2010 - Thomas Wagner
- bump to 4.3.2
- rework patch gmp-01 for version 4.3.2
- pause/remove Source1 for AMD64 assembly improvements (is this still needed?)
- use SunStudio for 64bit  (was gcc used for the Source1 AMD64 assembly improvements? pls speak up if you need this again)
- add patch2 extern inline (http://gmplib.org/list-archives/gmp-discuss/2010-February/004031.html)
* Sat Mar 14 2009 - Thomas Wagner
- shorten ACLOCAL flags by removing -I %{_datadir}/aclocal (fails if diry not present)
- fix packaging error by adding %_datadir to configure
- redefine %{_infodir} to be in /usr/gnu
- configure add %{bld_arch}
- add subdir to SUNW_BaseDir:            %{_basedir}/%{_subdir}
* Sun Feb 22 2009 - Thomas Wagner
- move to /usr/gnu and remove Conflicts: SUNWgnu-mp
* Sat Feb 21 2009 - Thomas Wagner
- add Conflicts: SUNWgnu-mp
* Tue Sep 02 2008 - halton.huo@sun.com
- Add /usr/share/aclocal to ACLOCAL_FLAGS to fix build issue
* Mon Feb 25 2008 - laca@sun.com
- fix sparcv9 build
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Remove Requires/BuildRequires to SFEreadline
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Fix amd64 build
* Sat Jun 30 2007 - nonsea@users.sourceforge.net
- Use http url in Source.
* Tue mar  7 2007 - dougs@truemail.co.th
- enabled 64-bit build and added speedup patch for AMD64
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEgmp
- bump to 4.2.1
- create devel subpkg
- update attributes
* Thu Nov 17 2005 - laca@sun.com
- create
