#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define	src_name	tor

Name:		SFEtor
IPS_Package_Name:	network/tor
Version:	0.2.2.34
Summary:	Anonymizing overlay network for TCP (The onion router)
URL:		https://www.torproject.org/
Group:		System Environment/Daemons
License:	3-clause BSD
Source:		http://www.torproject.org/dist/%{src_name}-%{version}.tar.gz
Source1:	tor.auth_attr
Source2:	tor.prof_attr
Source3:	tor.sh
Source4:	tor.xml
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWopenssl-include
Requires:	SUNWopenssl-libraries
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
./configure --prefix=%{_prefix}		\
	--sysconfdir=%{_sysconfdir}	\
	--with-tor-user=daemon		\
	--with-tor-group=daemon		\
	--with-libevent-dir=/usr/gnu

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

install -p -m 0755 contrib/torctl %{buildroot}%{_bindir}

install -d 0755 %{buildroot}%{_sysconfdir}/security/auth_attr.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/security/auth_attr.d/tor

install -d 0755 %{buildroot}%{_sysconfdir}/security/prof_attr.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/security/prof_attr.d/tor

install -d 0755 %{buildroot}%/lib/svc/method
install -m 0755 %{SOURCE3} %{buildroot}/lib/svc/method

install -d 0755 %{buildroot}%/lib/svc/manifest/network
install -m 0644 %{SOURCE4} %{buildroot}%/lib/svc/manifest/network

install -d 0700 %{buildroot}%{_localstatedir}/lib/tor
install -d 0755 %{buildroot}%{_localstatedir}/log/tor

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%doc INSTALL LICENSE README ChangeLog doc/HACKING doc/TODO
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/tor
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/tor/*
%{_mandir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/security
%{_sysconfdir}/tor
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0755, daemon, daemon) %{_localstatedir}/log/tor
%dir %attr (0755, root, other) %{_localstatedir}/lib
%dir %attr (0700, daemon, daemon) %{_localstatedir}/lib/tor
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0755, root, sys) /lib/svc/method/tor.sh
%class(manifest) %attr(0444, root, sys) /lib/svc/manifest/network/tor.xml

%changelog
* Thu Nov 17 2011 - Milan Jurik
- initial spec
