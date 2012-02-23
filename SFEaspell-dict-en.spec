#
# spec file for package SFEaspell-dict-en
#
# includes module(s): aspell-dict-en
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname aspell6-en

Name:                    SFEaspell-dict-en
IPS_Package_Name:	 text/aspell-dict-en
Summary:                 Aspell English Dictionary - GNU Aspell 0.60 English Dictionary Package
Group:                   Utility
Version:                 7.1
URL:		         http://aspell.net
Source:		         http://ftp.gnu.org/gnu/aspell/dict/en/%srcname-%version-0.tar.bz2
License: 		 Copyrighted
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:           SFEaspell-core

%description
This is the English dictionary for Aspell.  It requires Aspell 
version 0.60 or better.

%prep
rm -rf %name-%version-0
%setup -q -n %srcname-%version-0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --vars DESTDIR=%{_prefix} ASPELL=/usr/bin/aspell PREZIP=/usr/bin/prezip

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_libdir}
%{_libdir}/aspell-0.60/*

%changelog
* Wed Feb 22 2012- logan@gedanken.org
- Initial spec.
