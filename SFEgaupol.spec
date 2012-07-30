#
# spec file for package SFEgaupol
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
# Note: On Solaris, this often chews up my X server. I can get it back by 
# logging in remotely and killing the application. So... it's not perfect, 
# but it's here as a stopgap until totem gains (stable) ass/ssa support.
# YMMV.


%include Solaris.inc

%define pythonver 2.6

Name:		SFEgaupol
IPS_Package_Name:	media/subtitles/gaupol
Summary:	subtitle editor
Version:	0.19.2
License:	BSD
Group:		Applications/Sound and Video
URL:		http://home.gna.org/gaupol
Source:		http://download.gna.org/gaupol/0.19/gaupol-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-python26-libs
Requires: SUNWPython26
Requires: SUNWgnu-gettext
BuildRequires: SUNWgnome-python26-libs-devel
BuildRequires: SUNWPython26-devel

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n gaupol-%version

%build

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py clean install --prefix=/usr --root=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/gaupol
%{_mandir}/*
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gaupol/*
%attr (-, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/gaupol.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr(-,root,other) %{_datadir}/locale
%endif

%changelog
* Mon Feb 06 2012 - Milan Jurik
- bump to 0.19.2
* Sat May 08 2010 - jchoi42@pha.jhu.edu
- initial spec
