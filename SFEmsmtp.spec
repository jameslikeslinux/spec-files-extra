#
# spec file for package SFEmsmtp
#
#

%include Solaris.inc

Name:		SFEmsmtp
IPS_Package_Name:	mail/msmtp
Summary:	SMTP client for sending to a smart host
Group:		Applications/Internet
License:	GPLv3+
SUNW_Copyright:	msmtp.copyright
URL:		http://msmtp.sourceforge.net/
Meta(info.upstream):     Martin Lambers <marlam@marlam.de>
Version:	1.4.27
Source:		%{sf_download}/msmtp/msmtp-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:	SUNWgnutls
%include default-depend.inc

%description
msmtp is an SMTP client.
In the default mode, it transmits a mail to an SMTP server (for example at a free mail provider) which does the delivery.
To use this program with your mail user agent (MUA), create a configuration file with your mail account(s) and tell your MUA to call msmtp instead of /usr/sbin/sendmail.

Features include:

    * Sendmail compatible interface (command line options and exit codes).
    * Authentication methods PLAIN, LOGIN, CRAM-MD5, DIGEST-MD5, GSSAPI, and NTLM.
    * TLS/SSL both in SMTP-over-SSL mode and in STARTTLS mode. Full certificate trust checks can be performed. A client certificate can be sent.
    * Fast SMTP implementation using command pipelining.
    * Support for Internationalized Domain Names (IDN).
    * DSN (Delivery Status Notification) support.
    * RMQS (Remote Message Queue Starting) support (ETRN keyword).
    * IPv6 support.
    * Support for multiple accounts.

%prep
%setup -q -c -n %name-%version
cd msmtp-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
cd msmtp-%{version}
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
	    --without-libgsasl          \
	    --without-libidn
make -j$CPUS || make

%install
rm -rf $RPM_BUILD_ROOT
cd msmtp-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || {
    /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
}

%postun
[ ! -x /usr/sbin/fix-info-dir ] || {
    /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_infodir}
%{_mandir}

%changelog
* Sat Feb 04 2012 - Milan Jurik
- bump to 1.4.27
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Tue Apr 19 2011 - Knut Anders Hatlen
- Bumped to 1.4.23
- Removed /usr/share/info/dir because of collision with system/prerequisite/gnu
* Tue Mar 02 2010 - matt@greenviolet.net
- Initial spec file
