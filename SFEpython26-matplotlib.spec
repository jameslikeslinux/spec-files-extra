#
# spec file for package SFEmatplotlib
#
# includes module(s): matplotlib
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_url         %{sf_download}/matplotlib
%define src_name        matplotlib

Name:                   SFEpython26-matplotlib
Summary:                A plotting library for Python which uses syntax similar to MATLAB
URL:                    http://matplotlib.sourceforge.net
Version:                1.0.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWPython26
BuildRequires:           SUNWPython26-devel
Requires:               SFEpython26-numpy


%define python_version  2.6

%prep
%setup -q -n %{src_name}-%{version}

%build
export PYTHON="/usr/bin/python%{pythonver}"
export CC=gcc
export CXX=g++
export PYCC_CC="$CC"
export PYCC_CXX="$CXX"
#export CFLAGS="$CFLAGS -I/usr/include/python%{python_version}"
export CFLAGS="%optflags -I/usr/xpg4/include -I%{_includedir} -I/usr/include/python%{pythonver}"
#export CXXFLAGS="%gcc_cxx_optflags -I/usr/include/python%{python_version}"
#export LDFLAGS="%{_ldflags} -L%{_cxx_libdir} -R%{_cxx_libdir}"
export LDFLAGS="%_ldflags"

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Wed Mar 23 2011 - Thomas Wagner
- switch to SUNWpython26 and SFEpython26-numpy
- initial spec copied from SFEmatplotlib.spec
- bump to 1.0.1, adjust download-URL (remove http://)
* Tue Feb 11 2008 - Pradhap < pradhap (at) gmail.com >
- Fixed links
* Sun Feb 10 2008 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
