#
# spec file for package SFEbitlbee
#
# includes module(s): bitlbee
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%define _basedir /

%define srcname bitlbee

Name:                    SFEbitlbee
IPS_Package_Name:	 network/chat/bitlbee
Summary:                 BitlBee - An IRC to other chat networks gateway
Group:                   Utility
Version:                 3.0.5
URL:		         http://www.bitlbee.org
Source:		         http://get.bitlbee.org/src/bitlbee-%version.tar.gz
Source2:                 bitlbee.xml
License: 		 GPLv2
Patch1:                  bitlbee-01-ipc.diff
Patch2:                  bitlbee-02-irc_im.diff
Patch3:                  bitlbee-03-irc_commands.diff
Patch4:                  bitlbee-04-irc_user.diff
Patch5:                  bitlbee-05-makefile.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: library/security/openssl
Requires: library/glib2
Requires: SFElibotr

%description
BitlBee brings IM (instant messaging) to IRC clients. It is a great
solution for people who have an IRC client running all the time and
do not want to run an additional MSN/AIM/whatever client.

BitlBee currently supports the following IM networks/protocols:
XMPP/Jabber (including Google Talk), MSN Messenger, Yahoo! Messenger,
AIM and ICQ, and the Twitter microblogging network (plus all other
Twitter API compatible services like identi.ca and status.net).

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

#bitlbee manifest
cp -p %{SOURCE2} bitlbee.xml

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=/usr			\
	    --mandir=/usr/share/man		\
            --ssl=openssl                       \
            --otr=1

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-etc DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib/bitlbee/

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp bitlbee.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%actions
user ftpuser=false gcos-field="BitlBee Reserved UID" username="bitlbee" password=NP group="other"

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) /usr/sbin
/usr/sbin/*
%dir %attr(0755, root, bin) /usr/etc/bitlbee
/usr/etc/bitlbee/*
%dir %attr (0755, root, bin) /usr/share/man
%dir %attr (0755, root, bin) /usr/share/man/man5
/usr/share/man/man5/*
%dir %attr (0755, root, bin) /usr/share/man/man8
/usr/share/man/man8/*
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, sys) /usr/share/bitlbee
/usr/share/bitlbee/*

%dir %attr(0755, bitlbee, root) /var/lib/bitlbee
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/bitlbee.xml

%changelog
* Sat Apr 28 2012 - Logan Bruns <logan@gedanken.org>
- Fixed another permission and also changed to no longer enable service by default.
* Tue Apr 17 2012 - Logan Bruns <logan@gedanken.org>
- Fixed some permissions.
* Fri Mar 2 2012- Logan Bruns <logan@gedanken.org>
- New smf manifest, use a different runtime model and switch from gnutls to openssl.
* Thu Mar 1 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
