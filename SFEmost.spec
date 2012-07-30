#
# spec file for package SFEmost
#

%include Solaris.inc

Name:		SFEmost
IPS_Package_Name:	file/most
Summary:	most - a paging program that displays as many files at a time as possible
Group:		Applications/System Utilities
URL:		http://most.org/
Version:	5.0.0a
IPS_component_version: 5.0.0.1
Source:		ftp://space.mit.edu/pub/davis/most/most-%{version}.tar.bz2

SUNW_Copyright:		 %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWslang
Requires:      SUNWslang

%include default-depend.inc

%prep
%setup -q -n most-%version

%build

export CFLAGS="%optflags"
##export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


gmake

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}

#rename usr/share/most to usr/share/SFEmost
mv $RPM_BUILD_ROOT/%{_docdir}/most $RPM_BUILD_ROOT/%{_docdir}/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README changes.txt most.doc lesskeys.rc most.rc most-fun.txt
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Sun Apr 22 2012  - Thomas Wagner
- Initial spec
