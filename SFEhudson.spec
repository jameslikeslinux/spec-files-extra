#
# spec file for package SFEhudson
#
# includes module(s): hudson
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%define _basedir /

%define srcname hudson

Name:                    SFEhudson
IPS_Package_Name:	 developer/build/hudson
Summary:                 Hudson - Extensible continuous integration server
Group:                   Utility
Version:                 3.0.0
URL:		         http://hudson-ci.org
Source:		         http://download.eclipse.org/hudson/war/hudson-%{version}-M1.war
Source2:                 hudson.xml
Source3:                 hudson.sh
License: 		 Eclipse and Apache
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: runtime/java

%description
Hudson is a powerful and widely used open source continuous
integration server providing development teams with a reliable way to
monitor changes in source control and trigger a variety of
builds. Hudson excels at integrating with almost every tool you can
think of. Use Apache Maven, Apache Ant or Gradle or anything you can
start with a command line script for builds and send messages via
email, SMS, IRC and Skype for notifications.

In addition to providing a platform for continuous integration builds,
Hudson can also be extended to support software releases,
documentation, monitoring, and a number of use cases secondary to
continuous integration. In short, if you can think it, Hudson can do
it. From automating system administration tasks with Puppet and
verifying infrastructure setup with Cucumber, to building and testing
PHP code, to simply building Enterprise Java applications - Hudson
stands ready to help.

%prep
rm -rf %name-%version
mkdir %name-%version
cp %{SOURCE} hudson.war
cp %{SOURCE2} hudson.xml
cp %{SOURCE3} hudson.sh

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib/hudson
cp hudson.war $RPM_BUILD_ROOT/var/lib/hudson
cp hudson.sh $RPM_BUILD_ROOT/var/lib/hudson
chmod a+x $RPM_BUILD_ROOT/var/lib/hudson/hudson.sh
mkdir -p $RPM_BUILD_ROOT/var/log/hudson
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp hudson.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%actions
user ftpuser=false gcos-field="Hudson Reserved UID" username="hudson" password=NP group="other" home-dir="/var/lib/hudson"

%files
%defattr (-, hudson, bin)
%dir %attr(0755, hudson, root) /var/lib/hudson
/var/lib/hudson/*
%dir %attr(0755, hudson, root) /var/log/hudson
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/hudson.xml

%changelog
* Fri Mar 9 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
