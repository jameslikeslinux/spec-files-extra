#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:		SFEisomaster
IPS_Package_Name:	desktop/cd-burning/isomaster
Summary:	ISO editor
Group:		Applications/System Utilities
URL:		http://www.littlesvr.ca/isomaster/
License:	GPLv2
Version:	1.3.9
Source:		http://littlesvr.ca/isomaster/releases/isomaster-%{version}.tar.bz2
Patch1:		isomaster-01-w.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n isomaster-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

make -j$CPUS PREFIX=%{_prefix}

%install
rm -rf %{buildroot}
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf %{buildroot}%{_datadir}/locale
%endif

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/isomaster.desktop
%{_docdir}/*
%{_mandir}
%{_datadir}/isomaster

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Feb 04 2012 - Milan Jurik
- Initial spec
