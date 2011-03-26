#
# spec file for package SFEvnc2flv
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define python_version 2.6

Name:		SFEvnc2flv
Summary:	Desktop Screen Recorder for UNIX, Linux, Windows or Mac. 
Version:	20100207
URL:		http://www.unixuser.org/~euske/python/vnc2flv/
Source:		http://pypi.python.org/packages/source/v/vnc2flv/vnc2flv-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	SUNWpython26-setuptools
BuildRequires:	SUNWPython26
Requires:	SUNWPython26

%include default-depend.inc

%description
Vnc2flv is a screen recorder. It captures a VNC desktop session and saves it as a Flash Video (FLV) file.

%prep
%setup -q -n vnc2flv-%{version}

%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
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
%{_bindir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Sat Mar 26 2011 - Milan Jurik
- initial version
