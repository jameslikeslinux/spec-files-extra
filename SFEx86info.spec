#
# spec file for package SFEx86info
#
%include Solaris.inc
Name:		SFEx86info
IPS_Package_Name:	diagnostic/x86info
Summary:	x86info - tool for reading cpu cpabilities
URL:		http://www.codemonkey.org.uk/projects/x86info
Group:		Applications/System Utilities
Version:	1.21
Source:		http://codemonkey.org.uk/projects/x86info/old/x86info-%{version}.tgz
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright:	%{name}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc

%description
x86info, a CPU identification utility.

%prep
%setup -q -c -n %name-%version

%build
cd x86info-*

#nothing to configure, just "make"
make

%install
rm -rf $RPM_BUILD_ROOT

cd x86info-*
mkdir -p $RPM_BUILD_ROOT/usr/sbin
cp -p x86info $RPM_BUILD_ROOT/usr/sbin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*


%changelog
* Tue Aug 16 2011 - Thomas Wagner
- change Source URL, newer releases 1.22-1.29 need patching
* Sun Dev 21 2008 - Thomas Wagner
- remove snapshot-date
- bump to 1.21
* Wed Oct 17 2007 - laca@sun.com
- fix issues with snapshot date
* Sat Aug 04 2007 - Thomas Wagner
- Initial spec
