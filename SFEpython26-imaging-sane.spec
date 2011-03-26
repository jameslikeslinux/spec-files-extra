#
# spec file for package SUNWpython-imaging-sane
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define python_version 2.6

Name:		SFEpython26-imaging-sane
Summary:	The imaging-sane module is a Python interface to the SANE
Version:	1.1.7
URL:		http://www.pythonware.com/products/pil/
Source:		http://effbot.org/downloads/Imaging-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	SUNWpython26-setuptools
BuildRequires:	SUNWPython26
Requires:	SUNWPython26
BuildRequires:	SUNWsane-backendu
Requires:	SUNWsane-backendu

%include default-depend.inc

%description
The imaging-sane module is a Python interface to the SANE (Scanner Access is Now Easy) library, which provides access to various raster scanning devices such as flatbed scanners and digital cameras. 

%prep
%setup -q -n Imaging-%{version}

%build
cd Sane
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
cd Sane
python%{python_version} setup.py install -O1 --skip-build --root="$RPM_BUILD_ROOT" --prefix="%{_prefix}"

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Sat Mar 26 2011 - Milan Jurik
- initial version
