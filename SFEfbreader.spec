#
# spec file for package SFEfbreader.spec
#
# includes module(s): fbreader
#

%include Solaris.inc

%define src_name fbreader

Name:		SFEfbreader
IPS_Package_Name:	desktop/fbreader
Version:	0.12.10
Summary:	E-book reader
Group:		Applications/Publishing
License:	GPLv2
URL:		http://www.fbreader.org/
Source:		http://www.fbreader.org/files/sources/fbreader-sources-%{version}.tgz
Patch1:		fbreader-01-cflags.diff
Patch2:		fbreader-02-p.diff
Patch3:		fbreader-03-gcc46.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFElibfribidi-devel
Requires:	SFElibfribidi
BuildRequires:	SFEliblinebreak-devel
Requires:	SFEliblinebreak
BuildRequires:	SUNWcurl
Requires:	SUNWcurl
BuildRequires:	SUNWperl-xml-parser
Requires:	SUNWperl-xml-parser
BuildRequires:	SUNWgnome-common-devel

%description
FBReader is an e-book reader for various platforms.

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_bindir}/FBReader
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/FBReader
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/FBReader.desktop 
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/FBReader.png
%{_datadir}/pixmaps/FBReader
%{_datadir}/zlibrary

%changelog
* Thu Jul 15 2010 - Milan Jurik
- fix build and disable dynamic loading of UI module because of problem with libnspr4.so
* Sun Jul 11 2010 - Milan Jurik
- Initial spec
