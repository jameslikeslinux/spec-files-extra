#
# spec file for package SFEwxmaxima
#
# includes module(s): wxmaxima
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define srcname wxMaxima

Name:                    SFEwxmaxima
IPS_Package_Name:	 math/wxmaxima
Summary:                 wxMaxima - a Computer Algebra System
Group:                   Utility
Version:                 12.4.0
URL:		         http://wxmaxima.sourceforge.net
Source:		         %{sf_download}/project/wxmaxima/%{srcname}/12.04.0/%{srcname}-12.04.0.tar.gz
License: 		 GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEmaxima
Requires: SFEwxwidgets-gpp

%description
wxMaxima is a document based interface for the computer algebra system
Maxima. wxMaxima uses wxWidgets and runs natively on Windows, X11 and
Mac OS X. wxMaxima provides menus and dialogs for many common maxima
commands, autocompletion, inline plots and simple animations.

%prep
rm -rf %{srcname}-12.04.0
%setup -q -n %{srcname}-12.04.0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -R/usr/g++/lib"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --with-wx-config=/usr/g++/bin/wx-config

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
%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/wxMaxima
%{_datadir}/wxMaxima/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*

%changelog
* Mon Apr 30 2012 - Logan Bruns <logan@gedanken.org>
- Bumped to 12.04.0
* Mon Apr 16 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
