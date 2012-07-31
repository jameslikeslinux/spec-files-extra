#
# spec file for package SFEscalpel
#

%define src_name scalpel

%include Solaris.inc
Name:		SFEscalpel
IPS_Package_Name:	file/scalpel
Summary:	scalpel - A Frugal, High Performance File Carver
URL:		http://www.digitalforensicssolutions.com/Scalpel/
Version:	1.60
License:	GPLv2
SUNW_Copyright:	scalpel.copyright
Source:		http://www.digitalforensicssolutions.com/Scalpel/%{src_name}-%{version}.tar.gz
Patch1:		scalpel-01-add-SOLARIS-add-timersub.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# BuildRequires: SFEtre-devel
# Requires: SFEtre

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build

make solaris

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp -p %{src_name} $RPM_BUILD_ROOT/usr/bin/
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
cp -p %{src_name}.1 $RPM_BUILD_ROOT/usr/share/man/man1/
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{src_name}
cp -p %{src_name}.conf $RPM_BUILD_ROOT/usr/share/doc/%{src_name}/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_bindir}
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_mandir}


%changelog
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Wed Feb 23 2011 - Milan Jurik
- fix packaging (doc is not part of tarball)
* Sun May 18 2008  - Thomas Wagner
- Initial spec
