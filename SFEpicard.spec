#
# spec file for package: SFEpicard
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc

%define python_version 2.6

Name:		SFEpicard
Version:	0.14
Summary:	MusicBrainz Picard
License:	GPLv2
Url:		http://musicbrainz.org/doc/MusicBrainz_Picard
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright

Source0:	ftp://ftp.musicbrainz.org/pub/musicbrainz/picard/%{sname}-%{version}.tar.gz

%include default-depend.inc
BuildRequires:	SUNWPython26
BuildRequires:	SFEpyqt
BuildRequires:	SFEpython26-mutagen
BuildRequires:	SUNWlibdiscid-devel
BuildRequires:	SFEffmpeg-devel
BuildRequires:	SFElibofa
Requires:	SUNWPython26
Requires:	SFEpyqt
Requires:	SFEpython26-mutagen
Requires:	SUNWlibdiscid
Requires:	SFEffmpeg
Requires:	SFElibofa

Meta(info.maintainer):          James Lee <jlee@thestaticvoid.com>
Meta(info.upstream):            Lukáš Lalinský <lalinsky@gmail.com>
Meta(info.upstream_url):        http://musicbrainz.org/doc/MusicBrainz_Picard
Meta(info.classification):	org.opensolaris.category.2008:Applications/Sound and Video

%description
MusicBrainz Picard is a cross-platform (Linux/Mac OS X/Windows) application
written in Python and is the official MusicBrainz tagger. 

%prep
%setup -q -n %{sname}-%{version}

%build
python%{python_version} setup.py config

# This is an awful hack
# Python distutils on solaris always uses pycc to compile which
# causes c++ compilation to fail.  This sets the c compiler to CC
# so picard.util.astrcmp builds.  We have to force linking to libCrun
# because the library is dlopened by Python, which isn't linked to
# libCrun on Solaris.
CC=$CXX LDFLAGS="-lCrun" python%{python_version} setup.py build || true
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
%{_bindir}/picard
%{_libdir}/python%{python_version}/vendor-packages/picard
%{_libdir}/python%{python_version}/vendor-packages/picard-%{version}-py%{python_version}.egg-info
%attr(-,root,sys) %dir %{_datadir}
%attr(-,root,other) %dir %{_datadir}/applications
%{_datadir}/applications/picard.desktop
%attr(-,root,other) %{_datadir}/icons
%attr(-,root,other) %{_datadir}/locale

%changelog
* Tue Jun 28 2011 - James Lee <jlee@thestaticvoid.com>
- Prepare for SFE inclusion.
* Sat Feb 13 2010 - James Lee <jlee@thestaticvoid.com>
- Initial version
