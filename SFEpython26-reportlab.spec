#
# spec file for package SFEpython26-reportlab
#
# includes module(s): reportlab
#
%define src_name    reportlab
%define src_url     http://www.reportlab.org/ftp

%define python_version 2.6

%include Solaris.inc

Name:                SFEpython26-reportlab
IPS_Package_Name:	library/python-2/reportlab-26
Summary:             ReportLab Toolkit - PDF library for Python
URL:                 http://www.reportlab.org/
Version:             2.5
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython26-devel
Requires: SUNWPython26

%prep
%setup -q -n %{src_name}-%{version}

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Sun Mar 25 2012 - Milan Jurik
- bump to 2.5, move to python 2.6
* Mon Sep 24 2007 - trisk@acm.jhu.edu 
- Initial spec
