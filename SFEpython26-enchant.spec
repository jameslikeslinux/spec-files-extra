#
# spec file for package SFEpython26-enchant
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): pyenchant
#
%include Solaris.inc

%define python_version  2.6

%define src_name pyenchant
%define src_url http://pypi.python.org/packages/source/p/pyenchant/

Name:		SFEpython26-enchant
IPS_Package_Name:	library/python-2/python-enchant-26
Version:	1.6.5
Summary:	PyEnchant is a spellchecking library for Python, based on the excellent Enchant library
License:	LGPL
Group:		Development/Languages/Python
URL:		http://www.rfk.id.au/software/pyenchant/
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWPython26
Requires:	SUNWPython26
BuildRequires:	SUNWgnome-spell-devel
Requires:	SUNWgnome-spell

%prep
%setup -q -n pyenchant-%version

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot} --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p %{buildroot}%{_libdir}/python%{python_version}/vendor-packages
mv %{buildroot}%{_libdir}/python%{python_version}/site-packages/* \
   %{buildroot}%{_libdir}/python%{python_version}/vendor-packages/
rmdir %{buildroot}%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Sat Mar 26 2011 - Milan Jurik
- initial spec
