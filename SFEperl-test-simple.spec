#
# spec file for package: perl-Test-Simple
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc

Name:		SFEperl-test-simple
IPS_package_name: library/perl-5/test-simple
Version:	0.96
Summary:	Basic utilities for writing tests
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~mschwern/Test-Simple-%{version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/M/MS/MSCHWERN/Test-Simple-%{version}.tar.gz

BuildRequires:	SUNWperl584core
BuildRequires:	SUNWperl584usr
Requires:	SUNWperl584core
Requires:	SUNWperl584usr

Meta(info.maintainer):          taki@justplayer.com
Meta(info.upstream):            Michael G Schwern <mschwern@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~mschwern/Test-Simple-%{version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Basic utilities for writing tests
%prep
%setup -q -n Test-Simple-%{version}

%build
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
