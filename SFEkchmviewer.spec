#
# spec file for package SFEkchmviewer
#
# includes module: kchmviewer
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname kchmviewer

Name:		SFEkchmviewer
Summary:	CHM help file viewer based on Qt
URL:		http://www.kchmviewer.net
Vendor:		George Yunaev
Version:	5.2
License:	GPLv3+
SUNW_Copyright:	kchmviewer.copyright
Source:		http://downloads.sourceforge.net/%srcname/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires: SFEqt-gpp-devel
BuildRequires: SFEchmlib

Requires: SFEqt-gpp
Requires: SFEchmlib
Requires: SUNWzlib


%prep
gtar -xzf %SOURCE0
rm -fr %srcname-%version
mv build-%version %srcname-%version

%build
cd %srcname-%version

CPUS=$(psrinfo | awk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export PATH=/usr/g++/bin:$PATH
export QMAKESPEC=solaris-g++
export QTDIR=/usr/g++

qmake
# Parallelism breaks with 16 cpus, so don't use more than 4
gmake -j$(test $CPUS -ge 4 && echo 4 || echo $CPUS) PREFIX=%_basedir

%install
rm -rf $RPM_BUILD_ROOT

ginstall -d $RPM_BUILD_ROOT/%_bindir
ginstall -t $RPM_BUILD_ROOT/%_bindir %srcname-%version/bin/kchmviewer

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/%srcname


%changelog
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Wed Apr 13 2011 - Alex Viskovatoff
- Use only 2 cpus: using 16 cpus breaks build
* Sat Mar 12 2011 - Alex Viskovatoff
- Place /usr/stdcxx/bin at front of PATH
* Fri Jan 28 2011 - Alex Viskovatoff
- Accommodate to Qt being in /usr/stdcxx
* Mon Jan 24 2011 - Alex Viskovatoff
- Define QMAKESPEC
* Sat Dec 11 2010 - Alex Viskovatoff
- Initial spec
