#
# spec file for package: SFEperl-Proc-Daemon
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 0.06
Name:		SFEperl-proc-daemon
IPS_package_name: library/perl-5/proc-daemon
Version:	0.6
Summary:	Proc Daemon
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~ehood/Proc-Daemon-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/D/DE/DETI/Proc/Proc-Daemon-%{tarball_version}.tar.gz

BuildRequires:  %{pnm_buildrequires_perl_default}
Requires:  	%{pnm_requires_perl_default}

Meta(info.maintainer):          pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Earl Hood <ehood@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~ehood/Proc-Daemon-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description
Proc Daemon

%prep
%setup -q -n Proc-Daemon-%{tarball_version}

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
