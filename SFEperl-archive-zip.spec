#
# spec file for package: SFEperl-archive-zip
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 1.30
%define tarball_name    Archive-Zip

Name:		SFEperl-archive-zip
IPS_package_name: library/perl-5/archive-zip
Version:	1.30
IPS_component_version: 1.30
Summary:	Provides an interface to ZIP archive files
License:	Artistic
Url:		http://search.cpan.org/~adamk/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Archive-Zip-%{tarball_version}.tar.gz

BuildRequires:	%pnm_buildrequires_perl_default
Requires:	%pnm_requires_perl_default

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Adam Kennedy <adamk@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~adamk/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Provides an interface to ZIP archive files
%prep
%setup -q -n %{tarball_name}-%{tarball_version}

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
%{_prefix}/perl%{perl_major_version}
%dir %attr(0755,root,sys) %{_datadir}
%{_mandir}
%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%changelog
* Mon Sep 9 2011 - Thomas Wagner
- initial spec
