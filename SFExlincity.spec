#
# spec file for package SFExlincity
#

%include Solaris.inc

%define src_name lincity

Name:		SFExlincity
IPS_Package_Name:	games/lincity
Summary:	xlincity - Simulation game based on opensourced components of S*mc*ty. 
Group:		Game/Simulation
URL:		http://lincity.sourceforge.net 
Version:	1.12.1
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz 
Patch1:		xlincity-01-solaris.diff
SUNW_Copyright:	%{name}.copyright
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
%setup -q  -n %{src_name}-%{version} 
find ./intl -name \*.c -exec dos2unix {} {} \;
find ./intl -name \*.h -exec dos2unix {} {} \;
find ./intl -name \*.charset -exec dos2unix {} {} \;
%patch1 -p1

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}/*
%{_mandir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed May 19 2010 - Milan Jurik
- update to 1.12.1
* Wed Jan 23 2008 - Brian Nitz - <brian dot nitz at sun dot com> 
- Initial version.
