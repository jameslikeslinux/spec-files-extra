#
# spec file for package SFEcmake
#
# includes module(s): cmake
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

# Avoid conflict with SUNWcmake
%include usr-gnu.inc

Name:		SFEcmake
IPS_Package_Name:	sfe/developer/build/cmake 
Summary:	Cross platform make system
Version:	2.8.6
License:	BSD3c
SUNW_Copyright:	cmake.copyright
Source:		http://www.cmake.org/files/v2.8/cmake-%{version}.tar.gz
URL:		http://www.cmake.org
Group:		Development/Tools
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n cmake-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

./configure --prefix=%{_prefix} \
	    --bindir=%{_bindir}	\
	    --docdir=/share/doc/cmake \
	    --libdir=%{_libdir}	\
	    --mandir=/share/man

#If Ext2 Filesystem headers are present and found, compile errors occur
#disable this: HAVE_EXT2FS_EXT2_FS_H:INTERNAL=1
gsed -i -e 's/^HAVE_EXT2FS_EXT2_FS_H:INTERNAL=.*/HAVE_EXT2FS_EXT2_FS_H:INTERNAL=/' CMakeCache.txt 

gmake -j$CPUS

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/aclocal
%{_datadir}/cmake-*
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/cmake

%changelog
* Tue Oct 11 2011 - Thomas Wagner
- some sed don't support -i , change to "gsed" (and gmake)
* Tue Oct 11 2011 - Milan Jurik
- bump to 2.8.6, add IPS package name
* Wed Aug 24 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2.8.5
* Sat Mar  5 2011 - Alex Viskovatoff
- bump to 2.8.4; install documentation files in cmake's own directory
* Thu Feb 10 2011 - Thomas Wagner
- fix compile errors on (all) distros if configure thinks that EXT2 is present
  (archive_write_disk.c", line 2237: warning: implicit function declaration: _IOR)
* Thu Feb 10 2011 - Milan Jurik
- reintroducing and bump to 2.8.3
* Thu Oct 20 2008 - jedy.wang@sun.com
- Bump to 2.6.2
* Mon Aug 11 2008 - nonsea@users.sourceforge.net
- Bump to 2.6.1
* Tue May 13 2008 - nonsea@users.sourceforge.net
- Bump to 2.6.0
* Fri Mar 07 2008 - nonsea@users.sourceforge.net
- Bump to 2.4.8
* Mon Oct 22 2007 - nonsea@users.sourceforge.net
- Bump to 2.4.7
* Mon Mar 19 2007 - dougs@truemail.co.th
- Initial spec
