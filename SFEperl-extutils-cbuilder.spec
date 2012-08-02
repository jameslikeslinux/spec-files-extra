#
# spec file for package SFEperl-extutils-cbuilder
#
# includes module(s): ExtUtils-CBuilder
#

##TODO## IPS complatible version numbers!
%define module_version 0.2603
%define module_name ExtUtils-CBuilder
%define module_name_major ExtUtils
%define module_package_name extutils-cbuilder
#still unused: %define module_name_minor CBuilder


%include Solaris.inc
%include packagenamemacros.inc
Name:                    SFEperl-%{module_package_name}
Summary:                 %{module_name}-%{module_version} PERL module
Version:                 %{perl_version}.%{module_version}
Source:                   http://www.cpan.org/modules/by-module/%{module_name_major}/%{module_name}-%{module_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           %{pnm_buildrequires_perl_default}
Requires:                %{pnm_requires_perl_default}
BuildRequires:           %{pnm_buildrequires_SUNWsfwhea}

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q	-c -n %name-%version

%build
cd %{module_name}-%{module_version}
/usr/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL installdirs=vendor
CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC ./Build

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version}
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0

#rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

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
#%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/auto
#%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/auto/*
#%dir %attr(0755, root, sys) %{_datadir}
#%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%changelog
* Sat May 12 2012 - Thomas Wagner
- changed to use Build because old build system ended up in wrong
  target directories with perl 5.12
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- BuildRequires: %{pnm_buildrequires_SUNWsfwhea}
* Sat Jul 18 2009 - matt@greenviolet.net 
- Bump version to 0.2603
* Tue Apr 08 2008 - trisk@acm.jhu.edu
- Initial spec
