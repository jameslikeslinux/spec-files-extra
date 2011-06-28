#
# spec file for package: SFEsonata
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc

%define python_version 2.6

Name:		SFEsonata
Version:	1.6.2.1
Summary:	An elegant music client for MPD
License:	GPLv3
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://sonata.berlios.de/
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright

Source0:	http://download.berlios.de/sonata/%{sname}-%{version}.tar.bz2

%include default-depend.inc
BuildRequires:	SUNWgnu-gettext
BuildRequires:	SUNWgnome-common-devel
BuildRequires:	SUNWxwinc
BuildRequires:	SUNWPython26
BuildRequires:	SUNWgnome-python26-libs
BuildRequires:	SUNWgnome-python26-extras
BuildRequires:	SUNWdbus-python26
BuildRequires:	SFEpython26-mpd
Requires:	SUNWPython26
Requires:	SUNWgnome-python26-libs
Requires:	SUNWgnome-python26-extras
Requires:	SUNWdbus-python26
Requires:	SFEpython26-mpd

Meta(info.maintainer):          James Lee <jlee@thestaticvoid.com>
Meta(info.upstream):            Scott Horowitz <stonecrest@gmail.com>
Meta(info.upstream_url):        http://sonata.berlios.de/
Meta(info.classification):	org.opensolaris.category.2008:Applications/Sound and Video

%description
An elegant GTK+ client for the Music Player Daemon (MPD).

%prep
%setup -q -n %{sname}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
CFLAGS="-Immkeys" python%{python_version} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move to vendor-packages
if [ -d $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages ] ; then
	mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
	mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
		$RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
	rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages
fi

mkdir $RPM_BUILD_ROOT%{_docdir}
mv $RPM_BUILD_ROOT%{_datadir}/sonata $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}/sonata
%{_libdir}/python%{python_version}/vendor-packages/sonata
%{_libdir}/python%{python_version}/vendor-packages/Sonata-%{version}-py%{python_version}.egg-info
%{_libdir}/python%{python_version}/vendor-packages/mmkeys.so
%attr(755,root,sys) %dir %{_datadir}
%attr(755,root,other) %dir %{_datadir}/applications
%{_datadir}/applications/sonata.desktop
%{_mandir}/man1/sonata.1
%attr(755,root,other) %dir %{_docdir}
%{_docdir}/sonata
%attr(755,root,other) %dir %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%attr(-,root,other) %{_datadir}/locale


%changelog
* Tue Jun 28 2011 - James Lee <jlee@thestaticvoid.com>
- Prepare for SFE inclusion.
* Tue Dec 01 2009 - James Lee <jlee@thestaticvoid.com>
- Initial version.
