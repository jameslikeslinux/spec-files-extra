# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

# TODO:
#   fix manpages
#   ssh-http-proxy-connect
#   ssh-socks5-proxy-connect
#   RBAC
#   PAM

%include Solaris.inc

%define	src_name	openssh

Name:		SFEopenssh-server
IPS_Package_Name:	service/network/openssh
Summary:	Secure Shell protocol Server
Version:	6.1p1
IPS_Component_Version:	6.1.1
URL:		http://www.openssh.org/
Source:		http://ftp5.usa.openbsd.org/pub/OpenBSD/OpenSSH/portable/%{src_name}-%{version}.tar.gz
Source1:	ssh.xml
Source2:	sshd
Source3:	ssh-askpass
Group:		System/Security
License:	BSD
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
%include default-depend.inc
BuildRequires:	SFEldns-devel
Requires:	SFEldns
BuildRequires:	SUNWopenssl-include
Requires:	SUNWopenssl-libraries
BuildRequires:	SFEeditline-devel
Requires:	SFEeditline

%description
OpenSSH is a FREE version of the SSH connectivity tools that technical users of the Internet rely on. Users of telnet, rlogin, and ftp may not realize that their password is transmitted across the Internet unencrypted, but it is. OpenSSH encrypts all traffic (including passwords) to effectively eliminate eavesdropping, connection hijacking, and other attacks. Additionally, OpenSSH provides secure tunneling capabilities and several authentication methods, and supports all SSH protocol versions.

%package -n SFEopenssh-client
IPS_package_name:	network/openssh
Summary:	SSH Client and utilities
SUNW_BaseDir:	/
%include default-depend.inc
BuildRequires:	SFEldns-devel
Requires:	SFEldns
BuildRequires:	SUNWopenssl-include
Requires:	SUNWopenssl-libraries

%package -n SFEopenssh-common
IPS_package_name:	network/openssh/ssh-key
Summary:	Secure Shell protocol common Utilities
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix}	\
	--sysconfdir=%{_sysconfdir}/ssh	\
	--libexecdir=%{_libdir}/ssh	\
	--with-ssl-engine	\
	--with-pam		\
	--with-kerberos5=/usr	\
	--with-solaris-contracts	\
	--with-solaris-projects	\
	--with-xauth=/usr/bin/xauth	\
	--with-libedit		\
	--with-ldns

make -j$CPUS

%install
rm -rf %{buildroot}

gmake install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/lib/svc/manifest/network/
cp %{SOURCE1} %{buildroot}/lib/svc/manifest/network/
mkdir -p %{buildroot}/lib/svc/method/
cp %{SOURCE2} %{buildroot}/lib/svc/method/

cp %{SOURCE3} %{buildroot}/%{_libdir}/ssh/ssh-askpass

mv %{buildroot}/%{_sbindir}/sshd %{buildroot}/%{_libdir}/ssh/sshd
rmdir %{buildroot}/%{_sbindir}

# section 8 is not valid for Solaris
(cd %{buildroot}/%{_mandir}
    for i in `ls -1 man8/*`; do mv $i $(echo $i | sed 's/\.8/\.1m/g'); done
    for i in `ls -1 man8/fsck*`; do mv $i $( echo $i | sed 's/fsck\./fsck_/g' ); done
    for i in `ls -1 man8/mkfs*`; do mv $i $( echo $i | sed 's/mkfs\./mkfs_/g' ); done
    for i in `ls -1 man8/fsck_*[2-4].1m man8/mkfs_*[2-4].1m`; do mv $i $( echo $i | sed 's/\.1m/fs.1m/g' ); done
    mv man8 man1m
)

# section 5 is not valid for Solaris
(cd %{buildroot}/%{_mandir}
    for i in `ls -1 man5/*`; do mv $i $(echo $i | sed 's/\.5/\.4/g'); done
    mv man5 man4
)


%clean
rm -rf %{buildroot}

%pre
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/useradd -d /var/empty -s /bin/true -g sys sshd';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel sys';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions -n SFEopenssh-server
legacy desc="Secure Shell protocol Server" name="SSH Server, (Root)" pkg=SUNWsshdr
legacy desc="Secure Shell protocol Server" name="SSH Server, (Usr)" pkg=SUNWsshdu
user ftpuser=false gcos-field="sshd Reserved UID" username="sshd" password=NP group="sys" home-dir="/var/empty"

%actions -n SFEopenssh-client
legacy desc="Secure Shell protocol Client and associated Utilities" name="SSH Client and utilities, (Root)" pkg=SUNWsshr
legacy desc="Secure Shell protocol Client and associated Utilities" name="SSH Client and utilities, (Usr)" pkg=SUNWsshu

%actions -n SFEopenssh-common
legacy desc="Secure Shell protocol common Utilities" name="SSH Common, (Usr)" pkg=SUNWsshcu

%files -n SFEopenssh-server 
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/ssh
%class(preserve) %config %ips_tag(original_name=SUNWsshd:%{@}) %attr (0755, root, sys) %{_sysconfdir}/ssh/sshd_config
%dir %attr (0755, root, sys) /lib/svc/manifest
%dir %attr (0755, root, sys) /lib/svc/manifest/network
%class(manifest) %attr (0444, root, sys) /lib/svc/manifest/network/ssh.xml
%attr (0555, root, bin) /lib/svc/method/sshd
%dir %attr (0755, root, sys) %{_prefix}
%{_libdir}/ssh/sftp-server
%{_libdir}/ssh/sshd
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1m/sftp-server.1m
%{_mandir}/man1m/sshd.1m
%{_mandir}/man4/sshd_config.4
%dir %attr (0755, root, sys) %{_localstatedir}
%attr (0755, root, sys) %{_localstatedir}/empty

%files -n SFEopenssh-client
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/ssh
%attr (0755, root, sys) %{_sysconfdir}/ssh/moduli
%class(preserve) %config %ips_tag(original_name=SUNWssh:%{@}) %attr (0755, root, sys) %{_sysconfdir}/ssh/ssh_config
%dir %attr (0755, root, sys) %{_prefix}
%{_bindir}/scp
%{_bindir}/sftp
%{_bindir}/slogin
%{_bindir}/ssh
%{_bindir}/ssh-add
%{_bindir}/ssh-agent
%attr (0555, root, bin) %{_libdir}/ssh/ssh-askpass
%{_libdir}/ssh/ssh-pkcs11-helper
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/scp.1
%{_mandir}/man1/sftp.1
%{_mandir}/man1/slogin.1
%{_mandir}/man1/ssh.1
%{_mandir}/man1/ssh-add.1
%{_mandir}/man1/ssh-agent.1
%{_mandir}/man1m/ssh-pkcs11-helper.1m
%{_mandir}/man4/moduli.4
%{_mandir}/man4/ssh_config.4

%files -n SFEopenssh-common
%defattr (-, root, bin)
%{_bindir}/ssh-keygen
%{_bindir}/ssh-keyscan
%{_libdir}/ssh/ssh-keysign
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/ssh-keygen.1
%{_mandir}/man1/ssh-keyscan.1
%{_mandir}/man1m/ssh-keysign.1m

%changelog
* Fri Oct 12 2012 - Milan Jurik
- bump to 6.1p1
- force use of editline
* Fri Jun 8 2012 - Logan Bruns <logan@gedanken.org>
- Added a missing with_editline conditional which prevented compilation without editline
* Sat Jun 02 2012 - Milan Jurik
- Initial spec
