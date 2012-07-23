#
# spec file for package SFEbzr
#
# includes module(s): bzr
#
%include Solaris.inc

%define python_version 2.6

Name:		SFEbzr
IPS_Package_Name:	developer/versioning/bzr
Summary:	Bazaar Source Code Management System
License:	GPLv2+
SUNW_Copyright:	bzr.copyright
Group:		Development/Source Code Management
Version:	2.5.0
Source:		http://launchpad.net/bzr/2.5/%{version}/+download/bzr-%{version}.tar.gz
URL:		http://bazaar-vcs.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:	%{_prefix}
Requires: SUNWPython26
%include default-depend.inc
BuildRequires: SUNWPython26-devel


%description
Bazaar source code management system.

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -n bzr-%{version}

%build
export PYTHON="/usr/bin/python%{python_version}"
CFLAGS="$RPM_OPT_FLAGS"
/usr/bin/python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
/usr/bin/python%{python_version} setup.py install --prefix=$RPM_BUILD_ROOT%{_prefix}
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages

%if %build_l10n
%else
rm -rf %{buildroot}%{_datadir}/locale
%endif

# Delete optimized py code
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyo" -exec rm -f {} ';'
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/bzr.1

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Mar 28 2012 - knut.hatlen@oracle.com
- bump to 2.5.0
* Sun Dec 11 2011 - Milan Jurik
- bump to 2.4.2
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Tue Jul 19 2011 - brian.cameron@oracle.com
- Bump to 2.4.
* Fri May 13 2011 - knut.hatlen@oracle.com
- Fix Python 2.6 dependencies.
* Thu Apr 28 2011 - knut.hatlen@oracle.com
- Bump to 2.3.1.
* Mon Aug 23 2010 - brian.cameron@oracle.com
- Bump to 2.2.0.
* Sun Oct 11 2009 - brian.cameron@sun.com
- Bump to 2.0.0, and use Python 2.6.
* Fri Jul 31 2009 - halton.huo@sun.com
- Bump to 1.17
* Mon May 11 2009 - brian.cameron@sun.com
- Bump to 1.14.1
* Tue Sep 02 2008 - halton.huo@sun.com
- Bump to 1.6.1rc1
* Wed Jan  3 2007 - laca@sun.com
- bump to 0.13
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEbzr
- change to root:bin to follow other JDS pkgs.
* Sat Jan 7 2006  <glynn.foster@sun.com>
- initial version
