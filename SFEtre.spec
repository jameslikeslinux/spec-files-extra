#
# spec file for package SFEtre.spec
#
# includes module(s): TRE
#
%include Solaris.inc

%define src_name	tre
%define src_url		http://laurikari.net/tre
%define src_version	0.8.0

Name:		SFEtre
IPS_Package_Name:	library/libtre
Summary:	Lightweight, Robust, and Efficient POSIX compliant regexp matching library 
Version:	%{src_version}
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
URL:		http://laurikari.net/tre/
License:	BSD
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir}

%build
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}/lib*.so*
%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue July 20 2010 - markwright@internode.on.net
- bump to 0.8.0
* Sun Oct 14 2007 - laca@sun.com
- fix some directory attributes
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

