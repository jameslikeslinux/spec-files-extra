#
# spec file for package SFEperl-net-snmp
#
# includes module(s): Net-SNMP
#


%include Solaris.inc
%include packagenamemacros.inc

Name:		SFEperl-net-snmp
Version:	6.0.1
Summary:	Object oriented interface to SNMP
Group:		Development/Libraries
License:	Artistic
URL:		http://search.cpan.org/dist/Net-SNMP/
Source:		http://search.cpan.org/CPAN/authors/id/D/DT/DTOWN/Net-SNMP-v%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc

BuildRequires:	SFEperl-digest-sha1
Requires:	SFEperl-digest-sha1
BuildRequires:	SFEperl-crypt-des
Requires:	SFEperl-crypt-des

%description
The Net::SNMP module implements an object oriented interface to the
Simple Network Management Protocol.  Perl applications can use the
module to retrieve or update information on a remote host using the
SNMP protocol.  The module supports SNMP version-1, SNMP version-2c
(Community-Based SNMPv2), and SNMP version-3.  The Net::SNMP module
assumes that the user has a basic understanding of the Simple Network
Management Protocol and related network management concepts.


%prep
%setup -q	-c -n %name-%version
cd Net-SNMP-v%{version}

%build
cd Net-SNMP-v%{version}
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd Net-SNMP-v%{version}
make install

#remove unsed perllocal.pod
rm -r $RPM_BUILD_ROOT/%{_prefix}/lib
#remove unsed .packlist
rm -r $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*



%changelog
* Sat Aug  4 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- re-work build instructions
- use %include perl-depend.inc
- move out or perl/
- fix group for bindir
* Sat Mar 05 2011 - Milan Jurik
- initial spec
