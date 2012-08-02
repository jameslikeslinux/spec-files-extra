#
# spec file for package SFEjenkins
#
# includes module(s): jenkins
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%include packagenamemacros.inc

%define srcname jenkins
%define runuser jenkins
#use random number by userid tool %define runuserid jenkins
%define runusergroup other

Name:                    SFEjenkins
IPS_Package_Name:	 developer/build/jenkins
Summary:                 Jenkins - Extensible continuous integration server
Group:                   Utility
Version:                 1.475
URL:		         http://jenkins-ci.org
Source:		         http://mirrors.jenkins-ci.org/war/%{version}/jenkins.war
Source2:                 jenkins.xml
Source3:                 jenkins.sh
License: 		 MIT
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /var
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %pnm_requires_java_runtime_default

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

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

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Jenkins Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/jenkins"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for jenkins)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/jenkins %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for jenkins)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/jenkins %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c JENKINS


%files
%defattr (-, root, other)
%dir %attr(0755, root, other) /var/lib
%dir %attr(0755, jenkins, other) /var/lib/jenkins
%defattr (-, jenkins, other)
/var/lib/jenkins/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, jenkins, other) /var/log/jenkins


%files root
%defattr (-, root, sys)
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/jenkins.xml

%changelog
* Mon Jul 30 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.475.
* Sat Jun 23 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.471.
* Tue Apr 24 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.461.
* Tue Apr 24 2012 - Thomas Wagner
- merge with changes from local workspace Mar 31 2012
- set smf manifest to "disabled" by default
* Fri Apr 13 2012 - Logan Bruns <logan@gedanken.org>
- Switch to java package name macro and bump to 1.459.
* Sat Mar 31 2012 - Thomas Wagner
- add SVR4 %pre script for user creation, add -root package to get useradd before
  adding main package and manifest into _basedir=/, make base package _basedir=/var again
- use variable %{runuser} and %{runusergroup}, not used numeric %{runuserid}
- change BuildRequires to %{pnm_requires_java_runtime_default}, %include packagenamemacros.inc
* Sat Apr 7 2012 - Logan Bruns <logan@gedanken.org>
- Added a smf property to control max heap size.
* Wed Apr 4 2012 - Logan Bruns <logan@gedanken.org>
- Bump to 1.458.
* Mon Mar 26 2012 - Logan Bruns <logan@gedanken.org>
- Bump to 1.456.
* Tue Mar 13 2012 - Logan Bruns <logan@gedanken.org>
- Bump to 1.455.
* Fri Mar 9 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
