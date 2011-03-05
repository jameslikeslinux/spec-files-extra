#
# spec file for package SFEperl-net-snmp
#
# includes module(s): Net-SNMP
#

%define perl_version 5.8.4

%include Solaris.inc
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
%setup -q -n Net-SNMP-v%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor

make


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

mv %{buildroot}%{_prefix}/perl5/%{perl_version}/bin %{buildroot}%{_prefix}
install -d -m 0755 %{buildroot}%{_datadir}
mv %{buildroot}%{_prefix}/perl5/%{perl_version}/man %{buildroot}%{_datadir}
rmdir %{buildroot}%{_prefix}/perl5/%{perl_version}

%clean
rm -rf %{buildroot}


%files
%defattr(-, root, bin)
%doc Changes README
%{_bindir}
%{_prefix}/perl5
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_docdir}
%{_mandir}


%changelog
* Sat Mar 05 2011 - Milan Jurik
- initial spec
