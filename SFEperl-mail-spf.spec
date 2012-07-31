#
# spec file for package SFEperl-Mail-SPF
#
# includes module(s): Mail-SPF
#

#TODO# re-work perl specific prerequisites...

#note: download file version differs from package version (for IPS not accepting "015" / leading zero)
%define module_version 2.8.0

%define module_name Mail-SPF
%define module_name_major Mail
%define module_package_name mail-spf
#still unused: %define module_name_minor SPF


%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEperl-%{module_package_name}
Summary:                 %{module_name}-%{module_version} PERL module
Version:                 %{perl_version}.%{module_version}
Source:                  http://www.cpan.org/modules/by-module/%{module_name_major}/%{module_name}-v%{module_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SFEperl-version
BuildRequires:           SFEperl-module-build
BuildRequires:           SFEperl-uri
BuildRequires:           SFEperl-netaddr-ip

BuildRequires:  %{pnm_buildrequires_perl_default}
Requires:  	%{pnm_requires_perl_default}

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build
cd %{module_name}-v%{module_version}

#NOTE: this module might need more parameters set to place files in the place
/usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL installdirs=vendor

CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC ./Build


%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-v%{module_version}
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0

find %{buildroot} -name .packlist -exec %{__rm} {} \;

#%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/%{module_name_major}
%{_prefix}/%{perl_path_vendor_perl_version}/%{module_name_major}/*

#/usr/perl5/5.12/bin and /usr/perl5/5.12/man/man<1|3>
#/usr/perl5/5.8.4/bin and /usr/perl5/5.8.4/man/man<1|3>
%{_prefix}/perl%{perl_major_version}/%{perl_version}/*

#%dir %attr(0755, root, bin) %{_bindir}
#%{_bindir}/*
%dir %attr(0755, root, bin) %{_sbindir}
%{_sbindir}/*


%changelog
* Sat May 12 2012 - Thomas Wagner
- bump tp 2.8.0
- re-work Build system because old method failed to use correct locations
  for target directories completely
* Fri May 11 2012 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWsfwhea}, %include packagenamemacros.inc
- change (Build)Requires to %{pnm_buildrequires_perl_default}
* Thr Apr 30 2009 - Thomas Wagner
- Initial spec file
