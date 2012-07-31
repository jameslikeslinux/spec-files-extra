#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name smfgui

Name:		SFEsmfgui
IPS_Package_Name:	system/management/smfgui
Summary:	SMF GUI
Version:	0.9.5.3
URL:		http://smfgui.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}_%{version}_src.tar.gz
License:	CDDL
SUNW_copyright:	smfgui.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-common-devel

%prep
%setup -q -n %{src_name}_%{version}_src

%build
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp %{src_name} $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}

%changelog
- Tue Sep 27 2011 - Alex Viskovatoff
- add SUNW_copyright
* Tue Sep 27 2011 - Milan Jurik
- bump to 0.9.5.3
* Sat Mar 26 2011 - Milan Jurik
- initial spec
