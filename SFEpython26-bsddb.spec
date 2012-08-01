#
# spec file for package SFEpython-bsddb
#
# includes module(s): pybsddb
#
%include Solaris.inc

%define python_version  2.6

%define src_url http://pypi.python.org/packages/source/b/bsddb3/
%define src_name bsddb3

Name:		SFEpython26-bsddb
Summary:	Python wrappers for Berkeley DB
Version:	5.1.2
URL:		http://pybsddb.sourceforge.net
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:	SUNWPython26
BuildRequires:	SUNWPython26-devel
Requires:	SFEbdb
BuildRequires:	SFEbdb

%prep
%setup -q -n %{src_name}-%{version}

%build
python setup.py build --berkeley-db=/usr/gnu

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --berkeley-db=/usr/gnu --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Tue Jul 12 2012 - Milan Jurik
- include to SFE
* Thu Oct 11 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
