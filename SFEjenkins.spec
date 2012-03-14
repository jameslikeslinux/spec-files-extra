#
# spec file for package SFEjenkins
#
# includes module(s): jenkins
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%define _basedir /

%define srcname jenkins

Name:                    SFEjenkins
IPS_Package_Name:	 developer/build/jenkins
Summary:                 Jenkins - Extensible continuous integration server
Group:                   Utility
Version:                 1.455
URL:		         http://jenkins-ci.org
Source:		         http://mirrors.jenkins-ci.org/war/%{version}/jenkins.war
Source2:                 jenkins.xml
Source3:                 jenkins.sh
License: 		 MIT
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: runtime/java

%description
Jenkins is a powerful and widely used open source continuous
integration server providing development teams with a reliable way to
monitor changes in source control and trigger a variety of
builds. Jenkins excels at integrating with almost every tool you can
think of. Use Apache Maven, Apache Ant or Gradle or anything you can
start with a command line script for builds and send messages via
email, SMS, IRC and Skype for notifications.

In addition to providing a platform for continuous integration builds,
Jenkins can also be extended to support software releases,
documentation, monitoring, and a number of use cases secondary to
continuous integration. In short, if you can think it, Jenkins can do
it. From automating system administration tasks with Puppet and
verifying infrastructure setup with Cucumber, to building and testing
PHP code, to simply building Enterprise Java applications - Jenkins
stands ready to help.

%prep
rm -rf %name-%version
mkdir %name-%version
cp %{SOURCE} jenkins.war
cp %{SOURCE2} jenkins.xml
cp %{SOURCE3} jenkins.sh

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib/jenkins
cp jenkins.war $RPM_BUILD_ROOT/var/lib/jenkins
cp jenkins.sh $RPM_BUILD_ROOT/var/lib/jenkins
chmod a+x $RPM_BUILD_ROOT/var/lib/jenkins/jenkins.sh
mkdir -p $RPM_BUILD_ROOT/var/log/jenkins
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp jenkins.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%actions
user ftpuser=false gcos-field="Jenkins Reserved UID" username="jenkins" password=NP group="other" home-dir="/var/lib/jenkins"

%files
%defattr (-, root, other)
%dir %attr(0755, root, other) /var/lib
%dir %attr(0755, jenkins, root) /var/lib/jenkins
%defattr (-, jenkins, root)
/var/lib/jenkins/*
%dir %attr(0755, jenkins, root) /var/log/jenkins
%defattr (-, root, sys)
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/jenkins.xml

%changelog
* Tue Mar 13 2012 - Logan Bruns <logan@gedanken.org>
- Bump to 1.455.
* Fri Mar 9 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
