# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define	src_name	tor

Name:		SFEtor
IPS_Package_Name:	network/tor
Summary:	Anonymizing overlay network for TCP (The onion router)
Version:	0.2.2.35
URL:		http://www.torproject.org/
Source:		%{url}/dist/%{src_name}-%{version}.tar.gz
Source1:	tor.auth_attr
Source2:	tor.prof_attr
Source3:	tor.sh
Source4:	tor.xml
License:	Tor License
Group:		Applications/Internet
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %name-root
BuildRequires:	SFEasciidoc
BuildRequires:	SUNWopenssl-include
Requires:	SUNWopenssl-libraries
BuildRequires:	SUNWlibevent
Requires:	SUNWlibevent
BuildRequires:	SFElibevent2-devel
Requires:	SFElibevent2

%description
Tor is a connection-based low-latency anonymous communication system.

This package provides the "tor" program, which serves as both a client and
a relay node. Scripts will automatically create a "%{toruser}" user and
a "%{torgroup}" group, and set tor up to run as a daemon when the system
is rebooted.

Applications connect to the local Tor proxy using the SOCKS
protocol. The tor client chooses a path through a set of relays, in
which each relay knows its predecessor and successor, but no
others. Traffic flowing down the circuit is unwrapped by a symmetric
key at each relay, which reveals the downstream relay.

Warnings: Tor does no protocol cleaning.  That means there is a danger
that application protocols and associated programs can be induced to
reveal information about the initiator. Tor depends on Privoxy or 
similar protocol cleaners to solve this problem. This is alpha code,
and is even more likely than released code to have anonymity-spoiling
bugs. The present network is small -- this further reduces the
strength of the anonymity provided. Tor is not presently suitable
for high-stakes anonymity.

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}	\
	--sysconfdir=%{_sysconfdir}	\
	--with-libevent-dir=/usr/gnu	\
	--with-tor-user=tor	\
	--with-tor-group=daemon

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

install -p -m 0755 contrib/torctl %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/security/auth_attr.d/
cp %{SOURCE1} %{buildroot}/etc/security/auth_attr.d/%{src_name}
mkdir -p %{buildroot}/etc/security/prof_attr.d/
cp %{SOURCE2} %{buildroot}/etc/security/prof_attr.d/%{src_name}
mkdir -p %{buildroot}/lib/svc/method
cp %{SOURCE3} %{buildroot}/lib/svc/method/%{src_name}
mkdir -p %{buildroot}%{_localstatedir}/svc/manifest/site
cp %{SOURCE4} %{buildroot}%{_localstatedir}/svc/manifest/site/%{src_name}.xml
mkdir -p %{buildroot}%{_localstatedir}/log/%{src_name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{src_name}

%clean
rm -rf %{buildroot}

%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/groupadd daemon';
  echo '/usr/sbin/useradd -d %{_sysconfdir}/%{src_name} -s /bin/true -g daemon tor';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel tor';
  echo '/usr/sbin/groupdel daemon';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions
group groupname="tor"
user ftpuser=false gcos-field="TOR Reserved UID" username="tor" password=NP group="daemon"

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}
%{_mandir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}/security/auth_attr.d
%{_sysconfdir}/security/prof_attr.d
%config(noreplace) %{_sysconfdir}/tor/tor-tsocks.conf
%{_sysconfdir}/tor/torrc.sample
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/%{src_name}.xml
%dir %attr (0755, tor, daemon) %{_localstatedir}/log/%{src_name}
%dir %attr (0755, root, other) %{_localstatedir}/lib
%dir %attr (0700, daemon, daemon) %{_localstatedir}/lib/tor
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0555, root, bin) /lib/svc/method/%{src_name}.sh

%changelog
* Sat Feb 11 2012 - Milan Jurik
- Initial spec
