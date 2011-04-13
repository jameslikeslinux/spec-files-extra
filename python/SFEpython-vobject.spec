#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%define src_name vobject
%define python_version 2.6

%include Solaris.inc

%define src_version 0.8.1c

Name:                SFEpython-vobject
URL:                 http://vobject.skyhouseconsulting.com/
Summary:             vobject - a Python iCalendar library
Version:             0.8.1.0.3
Source:              http://vobject.skyhouseconsulting.com/%{src_name}-%{src_version}.tar.gz
Patch1:		     python-vobject-01-ez_setup.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWPython
Requires: SFEpython-dateutil
BuildRequires: SUNWPython-devel
BuildRequires: SUNWpython26-setuptools

%prep
%setup -q -n %{src_name}-%{src_version}
%patch1 -p0

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
/usr/bin/python%{python_version} ./setup.py install --root=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Sat Feb 05 2011 - Milan Jurik
- bump to 0.8.1c
* Tue Aug 26 2008 - halton.huo@sun.com
- Bump to 0.7.1
* Mon Mar 17 2008 - jijun.yu@sun.com
- Bump to 0.6.0
* Mon Feb 18 2008 - nonsea@users.sourceforge.net
- Bump to 0.5.0
* Fri Feb 15 2008 - jijun.yu@sun.com 
- add a build dependency: SFEpython-setuptools
* Tue Dec 11 2007 - nonsea@users.sourceforge.net
- Initial spec
