#
# spec file for package SFEderby
#
# includes module(s): derby
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define srcname db-derby

Name:                    SFEderby
IPS_Package_Name:	 database/derby
Summary:                 Derby - an open source relational database implemented entirely in Java
Group:                   Utility
Version:                 10.8.2.2
URL:		         http://db.apache.org/derby
Source:		         http://www.apache.org/dist/db/derby/%{srcname}-%{version}/%{srcname}-%{version}-bin.zip
License: 		 Apache License, Version 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %pnm_requires_java_runtime_default

%description
Apache Derby, an Apache DB subproject, is an open source relational
database implemented entirely in Java and available under the Apache
License, Version 2.0. Some key advantages include:

* Derby has a small footprint -- about 2.6 megabytes for the base
  engine and embedded JDBC driver.
* Derby is based on the Java, JDBC, and SQL standards.
* Derby provides an embedded JDBC driver that lets you embed Derby in
  any Java-based solution.
* Derby also supports the more familiar client/server mode with the
  Derby Network Client JDBC driver and Derby Network Server.
* Derby is easy to install, deploy, and use.

%prep
rm -rf %srcname-%version-bin
%setup -q -n %srcname-%version-bin

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/db-derby
cp -r * $RPM_BUILD_ROOT/usr/share/db-derby/
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -s %{_datadir}/db-derby/bin/ij $RPM_BUILD_ROOT/usr/bin/ij

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr(0755, root, sys) %{_datadir}/db-derby
%{_datadir}/db-derby/*
%defattr (-, root, bin)
%{_bindir}/ij

%changelog
* Mon Apr 16 2012 - Logan Bruns <logan@gedanken.org>
- Use java package names macro and fix some permissions
* Mon Mar 30 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
