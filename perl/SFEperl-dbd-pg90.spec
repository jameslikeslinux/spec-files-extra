#
# spec file for package: SFEperl-dbd-pg90
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc

Name:		SFEperl-dbd-pg90
IPS_package_name: library/perl-5/dbd-pg90
Version:	2.17.1
Summary:	Postgres Driver for DBI
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~turnstep/DBD-Pg-%{version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/T/TU/TURNSTEP/DBD-Pg-%{version}.tar.gz

BuildRequires:	SUNWperl584core
BuildRequires:	SUNWperl584usr
BuildRequires:	library/perl-5/version
BuildRequires:	library/perl-5/test-simple
BuildRequires:	library/perl-5/database
BuildRequires:	database/postgres-90/developer
BuildRequires:	database/postgres-90/library
Requires:	SUNWperl584core
Requires:	SUNWperl584usr
Requires:	library/perl-5/database
Requires:	database/postgres-90/library

Meta(info.maintainer):          taki@justplayer.com
Meta(info.upstream):            Greg Sabino Mullane <greg@turnstep.com>
Meta(info.upstream_url):        http://search.cpan.org/~turnstep/DBD-Pg-%{version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Postgres Driver for DBI
%prep
%setup -q -n DBD-Pg-%{version}

%build
POSTGRES_LIB="/usr/postgres/9.0/lib/"; export POSTGRES_LIB
perl Makefile.PL PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT LIB=/usr/perl5/vendor_perl/5.8.4 
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_datadir}/man/man3 $RPM_BUILD_ROOT%{_datadir}/man/man3perl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_prefix}/perl5
%attr(755,root,sys) %dir %{_datadir}
%{_mandir}
#%attr(755,root,sys) %dir %{_bindir}
#%{_bindir}/*

%changelog
