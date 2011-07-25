#
# spec file for package: SFEperl-xml-xpath
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 1.13
%define tarball_name    XML-XPath

Name:		SFEperl-xml-xpath
IPS_package_name: library/perl-5/xml-xpath
Group:		Development/Perl
Version:	1.13
IPS_component_version: 1.13
Summary:	A set of modules for parsing and evaluating
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~msergeant/%{tarball_name}-%{tarball_version}
SUNW_Copyright: perl-xml-xpath.copyright
SUNW_Basedir:	%{_basedir}
Source0:	http://search.cpan.org/CPAN/authors/id/M/MS/MSERGEANT/XML-XPath-%{tarball_version}.tar.gz

BuildRequires:	%pnm_buildrequires_perl_default
BuildRequires:	SUNWperl-xml-parser
Requires:	%pnm_requires_perl_default
Requires:	SUNWperl-xml-parser

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            MSERGEANT <msergeant@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~msergeant/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
A set of modules for parsing and evaluating
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
%dir %attr(0755,root,sys) %{_bindir}
%{_bindir}/xpath

%changelog
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Fri Jul  8 2011 - Alex Viskovatoff
- Change (Build)Requires to %{pnm_buildrequires_perl_default}
* Fri Mar  6 2011 - Alex Viskovatoff
- Generate new spec with make_perl_cpan_settings.pl
