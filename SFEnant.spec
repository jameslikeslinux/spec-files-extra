#
# spec file for package SFEnant
#
# includes module(s): nant
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname nant

Name:                    SFEnant
IPS_Package_Name:	 developer/build/nant
Summary:                 NAnt - A .NET Build Tool
Group:                   Utility
Version:                 0.92
URL:		         http://nant.sourceforge.net
Source:		         %{sf_download}/project/%{srcname}/%{srcname}/%{version}/%{srcname}-%{version}-bin.tar.gz
License: 		 GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SFEmono

%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/nant
mv bin doc examples schema *.txt $RPM_BUILD_ROOT/usr/share/nant
mkdir -p $RPM_BUILD_ROOT/usr/bin
echo "#!/bin/sh" > $RPM_BUILD_ROOT/usr/bin/nant
echo "/usr/mono/bin/mono /usr/share/nant/bin/NAnt.exe \$*" >> $RPM_BUILD_ROOT/usr/bin/nant
chmod 0755 $RPM_BUILD_ROOT/usr/bin/nant

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/nant
%{_datadir}/nant/*
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Mon Jun 25 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
