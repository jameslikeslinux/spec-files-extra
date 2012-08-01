#
# spec file for package: SFEperl-xml-parser
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 2.40
%define tarball_name    XML-Parser

Name:		SFEperl-xml-parser
IPS_package_name: library/perl-5/xml-parser
Group:		Development/Perl
Version:	2.40
IPS_component_version: 2.40
Summary:	Flexible fast parser with plug-in styles
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~coopercl/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
Source0:	http://search.cpan.org/CPAN/authors/id/C/CH/CHORNY/XML-Parser-%{tarball_version}.tar.gz

BuildRequires:	%pnm_buildrequires_perl_default
Requires:	%pnm_requires_perl_default

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Clark Cooper <clark@coopercc.net>
Meta(info.upstream_url):        http://search.cpan.org/~coopercl/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Flexible fast parser with plug-in styles
%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build
perl Makefile.PL PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT LIB=%_prefix/%perl_path_vendor_perl_version
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
%{_prefix}/%perl_path_vendor_perl_version
%dir %attr(0755,root,sys) %{_datadir}
%{_mandir}
#%dir %attr(0755,root,sys) %{_bindir}
#%{_bindir}/*

%changelog
* Fri Jul  8 2011 - Alex Viskovatoff
- Change (Build)Requires to %{pnm_buildrequires_perl_default}
* Fri Mar  6 2011 - Alex Viskovatoff
- Generate new spec with make_perl_cpan_settings.pl
