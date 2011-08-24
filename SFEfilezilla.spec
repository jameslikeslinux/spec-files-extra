#
# spec file for package SFEfilezilla
#
# includes module(s): filezilla
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%%use filezilla = filezilla.spec

Name:               SFEfilezilla
Summary:            FileZilla FTP client
Version:            %{filezilla.version}
SUNW_Copyright:     %{name}.copyright
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-vfs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnutls
Requires: SUNWgnu-idn
Requires: SUNWwxwidgets
Requires: SUNWxdg-utils
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnutls-devel
BuildRequires: SUNWgnu-idn
BuildRequires: SUNWwxwidgets-devel
BuildRequires: SUNWxdg-utils

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%filezilla.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CC=gcc
export CXX=g++
export CPPFLAGS="-I/usr/include/g++ -I%{_includedir}/idn"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -fpermissive"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
%filezilla.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%filezilla.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%doc(bzip2) -d filezilla-%{filezilla.version} COPYING GPL.html NEWS AUTHORS README
%doc -d filezilla-%{filezilla.version} ChangeLog
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/filezilla
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Aug 2009 - Gilles Dauphin
- back to libCstd, wx was compiled with it
* Aug 2009 - Gilles Dauphin
- use stlport4
* Thu Nov 13 2008 - alfred.peng@sun.com
- Depends on SUNWwxwigets and SUNWwxwigets-devel instead.
  Update the group bit.
* Sat Sep 27 2008 - alfred.peng@sun.com
- Add %doc to %files for copyright.
* Fri Aug 29 2008 - alfred.peng@sun.com
- Update %files to include icons.
* Thu Mar 06 2008 - nonsea@users.sourceforge.net
- Update %files cause version upgrade.
- Add pkg -l10n
- Repleace Requires/BuildRequires from SFElibidn to SUNWgnu-idn
* Mon Aug 06 2007 - nonsea@users.sourceforge.net
- initial version created
