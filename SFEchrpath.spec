#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:		SFEchrpath
IPS_Package_Name:       developer/chrpath
Summary:	allows you to modify the dynamic library load path
Group:		Development/Tools
Version:	0.14
Source:		http://alioth.debian.org/frs/download.php/3648/chrpath-%{version}.tar.gz
Patch1:		chrpath-01-solaris.diff
URL:		http://directory.fsf.org/wiki/Chrpath
License:	GPLv2+
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
'chrpath' allows you to modify the dynamic library load path (rpath and runpath) of compiled programs and libraries. 

%prep
%setup -q -n chrpath-%{version}
%patch1 -p1

%build
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}

make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
#Wrong destdir for docs
mv %{buildroot}%{_prefix}/doc %{buildroot}%{_docdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_mandir}/man1/chrpath.1

%changelog
* Sat Oct 29 2011 - Milan Jurik
- Initial spec
