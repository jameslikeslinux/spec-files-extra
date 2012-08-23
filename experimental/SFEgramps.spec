#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define python_version  2.6
%define src_name gramps

Name:		SFEgramps
Summary:	genealogy program 
Version:	3.2.6
URL:		http://gramps-project.org/
Source:		%{sf_download}/project/%{src_name}/Stable/%{version}/%{src_name}-%{version}.tar.gz
License:	GPLv2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWPython26
Requires:	SUNWPython26
Requires:	SFEpython26-bsddb

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export PYTHON=/usr/bin/python%{python_version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} --disable-mime-install

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/application-registry
%{_datadir}/application-registry/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/gramps
%dir %attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, root) %{_datadir}/mime/packages
%{_datadir}/mime/packages/*
%dir %attr (0755, root, other) %{_datadir}/mime-info
%{_datadir}/mime-info/*
%{_mandir}
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/gnome
%dir %attr (-, root, other) %{_datadir}/icons/gnome/48x48
%dir %attr (-, root, bin) %{_datadir}/icons/gnome/48x48/mimetypes
%{_datadir}/icons/gnome/48x48/mimetypes/*
%dir %attr (-, root, other) %{_datadir}/icons/gnome/scalable
%dir %attr (-, root, bin) %{_datadir}/icons/gnome/scalable/mimetypes
%{_datadir}/icons/gnome/scalable/mimetypes/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Mar 26 2011 - Milan Jurik
- initial spec
- needs fix for pybsddb mess
