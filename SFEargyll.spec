#
# spec file for package: argyll
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc

Name:		SFEargyll
Version:	1.3.3
Summary:	Argyll Color Management System
License:	AGPLv3
Url:		http://www.argyllcms.com/
SUNW_BaseDir:   %{_basedir}
SUNW_Copyright: %{name}.copyright

Source0:	http://www.argyllcms.com/Argyll_V%{version}_src.zip
Patch0:		argyll-01-solaris.diff

%include default-depend.inc
BuildRequires:	SFEjam
BuildRequires:	SUNWunzip
BuildRequires:	SUNWxwinc
BuildRequires:	SUNWxwplt
BuildRequires:	SUNWxorg-headers
BuildRequires:	SUNWxorg-clientlibs
BuildRequires:	SUNWlibusb
BuildRequires:  SUNWusbu
BuildRequires:	SUNWTiff-devel
Requires:	SUNWxwplt
Requires:	SUNWxorg-clientlibs
Requires:	SUNWlibusb
Requires:	SUNWTiff

Meta(info.maintainer):		James Lee <jlee@thestaticvoid.com>
Meta(info.upstream):		Graeme Gill <graeme@argyllcms.com>
Meta(info.upstream_url):	http://www.argyllcms.com/
Meta(info.classification):	org.opensolaris.category.2008:Applications/Graphics and Imaging

%description
ArgyllCMS is an ICC compatible color management system, available as Open
Source. It supports accurate ICC profile creation for scanners, cameras and
film recorders, and calibration and profiling of displays and RGB & CMYK
printers.

%prep
%setup -q -n Argyll_V%{version}
%patch0 -p1

%build
export LINKFLAGS="-L/usr/lib -pg"
jam -f Jambase

%install
rm -rf $RPM_BUILD_ROOT
jam -f Jambase install

rm bin/License.txt
mkdir -p $RPM_BUILD_ROOT%{_basedir}
cp -r bin $RPM_BUILD_ROOT%{_basedir}

mkdir -p $RPM_BUILD_ROOT%{_docdir}/argyll
cp -r doc $RPM_BUILD_ROOT%{_docdir}/argyll/html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %{_bindir}
%{_bindir}/applycal
%{_bindir}/average
%{_bindir}/cb2ti3
%{_bindir}/ccmxmake
%{_bindir}/cctiff
%{_bindir}/chartread
%{_bindir}/collink
%{_bindir}/colprof
%{_bindir}/dispcal
%{_bindir}/dispread
%{_bindir}/dispwin
%{_bindir}/extracticc
%{_bindir}/extractttag
%{_bindir}/fakeCMY
%{_bindir}/fakeread
%{_bindir}/greytiff
%{_bindir}/iccdump
%{_bindir}/iccgamut
%{_bindir}/icclu
%{_bindir}/illumread
%{_bindir}/invprofcheck
%{_bindir}/kodak2ti3
%{_bindir}/mppcheck
%{_bindir}/mpplu
%{_bindir}/mppprof
%{_bindir}/printcal
%{_bindir}/printtarg
%{_bindir}/profcheck
%{_bindir}/refine
%{_bindir}/revfix
%{_bindir}/scanin
%{_bindir}/sepgen
%{_bindir}/spec2cie
%{_bindir}/specplot
%{_bindir}/splitti3
%{_bindir}/spotread
%{_bindir}/spyd2en
%{_bindir}/synthcal
%{_bindir}/synthread
%{_bindir}/targen
%{_bindir}/tiffgamut
%{_bindir}/timage
%{_bindir}/txt2ti3
%{_bindir}/verify
%{_bindir}/viewgam
%{_bindir}/xicclu
%attr(-,root,sys) %dir %{_datadir}
%attr(-,root,other) %dir %{_docdir}
%{_docdir}/argyll

%changelog
* Mon Jun 13 2011 - jlee@thestaticvoid.com
- Update for SFE inclusion. 
* Thu Apr 22 2010 - jlee@thestaticvoid.com
- Initial version
