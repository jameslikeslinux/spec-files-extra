#
# spec file for package SFEpython26-mutagen
#
# includes module(s): mutagen
#
%include Solaris.inc

%define src_url         http://mutagen.googlecode.com/files
%define src_name        mutagen

Name:                   SFEpython26-mutagen
IPS_Package_Name:	library/python-2/python-mutagen-26
Summary:                Mutagen - A Python module to handle audio metadata
URL:                    http://www.sacredchao.net/quodlibet/wiki/Development/Mutagen
Version:                1.20
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython26
BuildRequires:          SUNWPython26-devel

%define python_version  2.6

%prep
%setup -q -n %{src_name}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Wed Aug 01 2012 - James Lee <jlee@thestaticvoid.com>
- Add IPS package name.
* Mon Nov 14 2011 - James Lee <jlee@thestaticvoid.com>
- Correct dependency on SUNWPython26
* Tue Dec 28 2010 - James Lee <jlee@thestaticvoid.com>
- Bump to 1.20.
- Build for Python 2.6.
* Tue Dec 25 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
