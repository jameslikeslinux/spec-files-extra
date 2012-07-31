#
# spec file for package: SFEperl-appconfig
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

Name:		SFEperl-appconfig
IPS_package_name: library/perl-5/appconfig
Version:	1.66
Summary:	Application config (from ARGV, file, ...)
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~abw/AppConfig-%{version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/A/AB/ABW/AppConfig-%{version}.tar.gz
BuildRequires:  %{pnm_buildrequires_perl_default}
Requires:  	%{pnm_requires_perl_default}


Meta(info.maintainer):          taki@justplayer.com
Meta(info.upstream):            Andy Wardley <cpan@wardley.org>
Meta(info.upstream_url):        http://search.cpan.org/~abw/AppConfig-%{version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Application config (from ARGV, file, ...)
%prep
%setup -q -n AppConfig-%{version}

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
%attr(755,root,sys) %dir %{_datadir}
%{_mandir}
#%attr(755,root,sys) %dir %{_bindir}
#%{_bindir}/*

%changelog
* Sat Aug  6 2011 - Thomas Wagner
- add pnm_macro to Makefile.PL LIB= and %files
- initial spec from taki@justplayer.com
