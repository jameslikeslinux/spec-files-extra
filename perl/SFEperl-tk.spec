#
# spec file for package: SFEperl-tk
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

# Created by experimental/make_perl_cpan_settings.pl

%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 804.029
%define tarball_name    Tk

Name:		SFEperl-tk
#IPS_package_name: library/perl-5/tk
Version:	804.029
IPS_component_version: 804.29
Summary:	a graphical user interface toolkit for Perl
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~tkml/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
#SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/S/SR/SREZIC/Tk-%{tarball_version}.tar.gz

BuildRequires:	%pnm_buildrequires_perl_default
BuildRequires:	SUNWTk
Requires:	%pnm_requires_perl_default
Requires:	SUNWTk

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            The Tk Perl Mailing list <ptk@lists.stanford.edu>
Meta(info.upstream_url):        http://search.cpan.org/~tkml/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
a graphical user interface toolkit for Perl
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
%attr(755,root,sys) %dir %{_datadir}
%{_mandir}
%{_bindir}

%changelog
* Fri Jul  8 2011 - Alex Viskovatoff
- Change (Build)Requires to %{pnm_buildrequires_perl_default}
* Sun Mar 20 2011 - Alex Viskovatoff
- Initial spec
