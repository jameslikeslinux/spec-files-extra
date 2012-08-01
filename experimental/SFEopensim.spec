#
# spec file for package SFEopensim
#
# includes module(s): opensim
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc

%define srcname opensim
%define runuser opensim
#use random number by userid tool %define runuserid opensim
%define runusergroup other

Name:                    SFEopensim
IPS_Package_Name:	 games/opensim
Summary:                 OpenSimulator - an open source multi-user 3D application server
Group:                   Applications/Games
Version:                 0.7.3.1
URL:		         http://opensimulator.org
Source:		         http://opensimulator.org/dist/opensim-%{version}-source.tar.gz
Source2:                 opensim.xml
Source3:                 opensim.sh
License: 		 BSD
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            /var
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEmono
Requires: SFEmono
BuildRequires: SFEopenjpeg-devel
Requires: SFEopenjpeg
BuildRequires: SFEnant

Requires: %name-root

#delivers username and SMF manifest
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/

%description
OpenSimulator is an open source multi-platform, multi-user 3D
application server. It can be used to create a virtual environment (or
world) which can be accessed through a variety of clients, on multiple
protocols. OpenSimulator allows virtual world developers to customize
their worlds using the technologies they feel work best - we have
designed the framework to be easily extensible.

Out of the box, OpenSimulator can be used to simulate virtual
environments similar to Second Life, given that it supports the core
of SL's messaging protocol. As such, these virtual worlds can be
accessed with the regular SL viewers. However, OpenSimulator is
neither a clone of Second Life's server nor does it aim at becoming
such a clone. On the contrary, OpenSimulator lacks support for many of
the game-specific features of Second Life (on purpose), while pursuing
innovative directions towards becoming the bare bones, but extensible,
server of the 3D Web.

%prep
rm -rf %name-%version
%setup -q -n %{srcname}-%{version}-source
cp %{SOURCE2} opensim.xml
cp %{SOURCE3} opensim.sh

%build
PATH=$PATH:/usr/mono/bin 
export PATH
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib
gsed -i 's|mono|/usr/mono/bin/mono|g' bin/opensim-ode.sh
# ugly hack to work around not be able to use spaces in ips packages
find bin -name "* *" -print | awk '{printf "mv \"%s\" \"`echo %s | tr \\  ^`\"\n", $0, $0}' | bash 
find bin -name .keep -exec rm {} \;
rmdir bin/Library
rmdir bin/Regions
rm bin/lib*/*.so bin/lib*/*.dll bin/lib*/*.dylib
mv bin $RPM_BUILD_ROOT/var/lib/opensim
ln -s /usr/lib/libsqlite3.so $RPM_BUILD_ROOT/var/lib/opensim/lib32/libsqlite3_32.so
chmod a+x opensim.sh
cp opensim.sh $RPM_BUILD_ROOT/var/lib/opensim
mkdir -p $RPM_BUILD_ROOT/var/log/opensim
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp opensim.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%actions
#you my at the top of the file %define runuserid (numeric) and add here: uid=%{runuserid}
user ftpuser=false gcos-field="Opensim Reserved UID" username="%{runuser}" password=NP group="other" home-dir="/var/lib/opensim"


%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo '/usr/bin/getent passwd %{runuser} >/dev/null || {';
#  echo 'echo "Adding %{runuser} user with numeric id %{runuserid} to system (for opensim)"';
#  echo '/usr/sbin/useradd -u %{runuserid} -g %{runusergroup} -G mail -d %{_localstatedir}/lib/opensim %{runuser}';
  echo 'echo "Adding %{runuser} user to system (for opensim)"';
  echo '/usr/sbin/useradd -g %{runusergroup} -G mail -d %{_localstatedir}/lib/opensim %{runuser}';
  echo '}';
  echo 'exit $retval' ) | $BASEDIR/var/lib/postrun/postrun -c OPENSIM


%files
%defattr (-, root, other)
%dir %attr(0755, root, other) /var/lib
%dir %attr(0755, opensim, other) /var/lib/opensim
%defattr (-, opensim, other)
/var/lib/opensim/*
%dir %attr (0755, root, sys) /var/log
%dir %attr(0755, opensim, other) /var/log/opensim

%files root
%defattr (-, root, sys)
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/opensim.xml

%changelog
* Wed Aug 1 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
