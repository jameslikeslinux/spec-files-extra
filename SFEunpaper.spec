#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name unpaper

Name:		SFEunpaper
Summary:	unpaper - post-processing scanned and photocopied book pages
Version:	0.3
URL:		http://unpaper.berlios.de/
Source:		http://download.berlios.de/unpaper/%{src_name}-bin-%{version}.tar.gz
License:	GPLv2
SUNW_Copyright:	unpaper.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
cc %{optflags} %{_ldflags} -lm -o unpaper src/unpaper.c

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
* Mon Jul 25 2011 - N.B.Prashanth
- add SUNW_Copyright
* Sat Mar 26 2011 - Milan Jurik
- initial spec
