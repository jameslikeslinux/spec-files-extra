#
# spec file for package: perl-Test-Simple
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

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

BuildRequires:  %{pnm_buildrequires_perl_default}
Requires:  	%{pnm_requires_perl_default}

Meta(info.maintainer):          taki@justplayer.com
Meta(info.upstream):            Michael G Schwern <mschwern@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~mschwern/Test-Simple-%{version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Basic utilities for writing tests
%prep
%setup -q -n Test-Simple-%{version}

%build
perl Makefile.PL PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT LIB=%{_prefix}/%{perl_path_vendor_perl_version}
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
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr(0755, root, sys) /usr/share
%{_mandir}
#%attr(755,root,bin) %dir %{_bindir}
#%{_bindir}/*

%changelog
* Sat Aug  6 2011 - Thomas Wagner
- add pnm_macro to Makefile.PL LIB= and %files
- initial spec from taki@justplayer.com
