#
# spec file for package: python26-mpd
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc

%define python_version 2.6

Name:		SFEpython26-mpd
Version:	0.3.0
Summary:	Python MPD Library
Group:		Development/Python
License:	GPLv3
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://jatreuman.indefero.net/p/python-mpd/
SUNW_Copyright: python-mpd.copyright
SUNW_Basedir:	%{_basedir}

Source0:	http://pypi.python.org/packages/source/p/python-mpd/python-mpd-%{version}.tar.bz2

%include default-depend.inc
BuildRequires:	SUNWPython26
Requires:	SUNWPython26

Meta(info.maintainer):          James Lee <jlee@thestaticvoid.com>
Meta(info.upstream):            J. Alexander Treuman <jat@spatialrift.net>
Meta(info.upstream_url):        http://jatreuman.indefero.net/p/python-mpd/
Meta(info.classification):	org.opensolaris.category.2008:Development/Python

%description
An MPD (Music Player Daemon) client library written in pure Python.

%prep
%setup -q -n python-mpd-%{version}

%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move to vendor-packages
if [ -d $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages ] ; then
	mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
	mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
		$RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
	rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %{_libdir}
%dir %{_libdir}/python%{python_version}
%dir %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/mpd.py
%{_libdir}/python%{python_version}/vendor-packages/mpd.pyc
%{_libdir}/python%{python_version}/vendor-packages/python_mpd-%{version}-py%{python_version}.egg-info

%changelog
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Thu Jun 30 2011 - Alex Viskovatoff
- Bump to 0.3.0
* Tue Dec 01 2009 - jlee@thestaticvoid.com
- Initial version
