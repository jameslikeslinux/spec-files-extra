#
# spec file for package SFEmaven
#
# includes module(s): maven
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define srcname maven

Name:                    SFEmaven
IPS_Package_Name:	 developer/build/maven
Summary:                 Maven - a software project management and comprehension tool
Group:                   Utility
Version:                 3.0.4
URL:		         http://maven.apache.org
Source:		         http://www.us.apache.org/dist/%{srcname}/binaries/apache-%{srcname}-%{version}-bin.tar.gz
License: 		 Apache License, Version 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %pnm_requires_java_runtime_default

%description
Apache Maven is a software project management and comprehension
tool. Based on the concept of a project object model (POM), Maven can
manage a project's build, reporting and documentation from a central
piece of information.

%prep
rm -rf apache-%srcname-%version
%setup -q -n apache-%srcname-%version

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/maven
cp -r * $RPM_BUILD_ROOT%{_datadir}/maven/
sed -e 's|/etc/mavenrc|/usr/share/maven/etc/mavenrc|g' \
  < bin/mvn > $RPM_BUILD_ROOT%{_datadir}/maven/bin/mvn
mkdir $RPM_BUILD_ROOT/%{_datadir}/maven/etc
echo M2_HOME=%{_datadir}/maven > $RPM_BUILD_ROOT%{_datadir}/maven/etc/mavenrc
echo JAVA_HOME=/usr/java >> $RPM_BUILD_ROOT%{_datadir}/maven/etc/mavenrc
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -s %{_datadir}/maven/bin/mvn $RPM_BUILD_ROOT/usr/bin/mvn

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/maven
%{_datadir}/maven/*
%defattr (-, root, bin)
%{_bindir}/mvn

%changelog
* Sun Jun 24 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
