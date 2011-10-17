#
# spec file for package SFEforemost
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:           SFEforemost
IPS_Package_Name:	system/file-system/foremost
Summary:        Foremost is a console program to recover files based on their headers, footers, and internal data structures
Version:        1.5.7
URL:		http://foremost.sourceforge.net/
Source:		http://foremost.sourceforge.net/pkg/foremost-%{version}.tar.gz
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc

%package root
Summary:	%{name} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%prep
%setup -q -n foremost-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

make solaris

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_bindir}
install -m 755 foremost %{buildroot}/%{_bindir}

mkdir -p %{buildroot}/%{_mandir}
gzcat foremost.8.gz > foremost.1
install -m 444 foremost.1 %{buildroot}/%{_mandir}/man1

mkdir -p %{buildroot}/%{_sysconfdir}
install -m 444 foremost.conf %{buildroot}/%{_sysconfdir}

mkdir -p %{buildroot}/%{_docdir}/foremost
install -m 444 README %{buildroot}/%{_docdir}/foremost

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/foremost
%{_mandir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Mon Oct 17 2011 - Milan Jurik
- add IPS package name
* Mon Feb 23 2011 - Milan Jurik
- Initial spec
