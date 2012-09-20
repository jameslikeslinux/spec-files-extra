#
# spec file for package SFEgerrit
#
# includes module(s): gerrit
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%include packagenamemacros.inc

%define srcname gerrit
%define runuser gerrit
#use random number by userid tool %define runuserid gerrit
%define runusergroup other

Name:                    SFEgerrit
IPS_Package_Name:	 developer/versioning/gerrit
Summary:                 Gerrit - Web based code review and project management
Group:                   Utility
Version:                 2.4.2
URL:		         http://gerrit.googlecode.com
Source:		         http://gerrit.googlecode.com/files/gerrit-%{version}.war
Source2:                 gerrit.xml
Source3:                 gerrit.sh
License: 		 Apache License 2.0
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
Gerrit is a web based code review system, facilitating online code
reviews for projects using the Git version control system.

Gerrit makes reviews easier by showing changes in a side-by-side
display, and allowing inline comments to be added by any reviewer.

Gerrit simplifies Git based project maintainership by permitting any
authorized user to submit changes to the master Git repository, rather
than requiring all approved changes to be merged in by hand by the
project maintainer. This functionality enables a more centralized
usage of Git.

%prep
rm -rf %name-%version
mkdir %name-%version
cp %{SOURCE} gerrit.war
cp %{SOURCE2} gerrit.xml
cp %{SOURCE3} gerrit.sh

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib/gerrit
cp gerrit.war $RPM_BUILD_ROOT/var/lib/gerrit
cp gerrit.sh $RPM_BUILD_ROOT/var/lib/gerrit
chmod a+x $RPM_BUILD_ROOT/var/lib/gerrit/gerrit.sh
mkdir -p $RPM_BUILD_ROOT/var/log/gerrit
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp gerrit.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Gerrit Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/gerrit"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for gerrit)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/gerrit %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for gerrit)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/gerrit %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c GERRIT


%files
%defattr (-, root, other)
%dir %attr(0755, root, other) /var/lib
%dir %attr(0755, gerrit, other) /var/lib/gerrit
%defattr (-, gerrit, other)
/var/lib/gerrit/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, gerrit, other) /var/log/gerrit


%files root
%defattr (-, root, sys)
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/gerrit.xml

%changelog
* Thu Sep 20 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
