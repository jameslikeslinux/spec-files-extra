#
# spec file for package SFEgrsync
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

Summary:	GTK+ frontend for rsync 
IPS_Package_Name:	desktop/network/grsync
Name:		SFEgrsync
Version:	1.2.0
License:	GPLv2
URL:		http://www.opbyte.it/grsync/
Source:		http://www.opbyte.it/release/grsync-%{version}.tar.gz
Patch1:		grsync-01-wall.diff
Group: System Environment/Daemons
BuildRoot:	%{_tmppath}/unbound-%{version}-build
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright:	grsync.copyright
%include default-depend.inc
Requires:	SUNWrsync

%description
Grsync is used to synchronize folders, files and make backups.

%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%name

%prep
%setup -q -n grsync-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf %{buildroot}%{_datadir}/locale
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,bin)
%{_bindir}
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/grsync
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/man1
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (-, root, root) %{_datadir}/mime
%attr (-, root, root) %{_datadir}/mime/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/mimetypes/
%{_datadir}/icons/hicolor/48x48/mimetypes/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Aug 01 2011 - Milan Jurik
- bump to 1.2.0
* Tue Feb 12 2008 - Ananth Shrinivas <ananth@sun.com>
- Initial spec
