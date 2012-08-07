#
# spec file for package SFEperl-razor
#
# includes module(s): Razor
#

##TODO## needs some cleaning (moving around directory in install probably can be cleaned up)

%define module_version 2.84
%define module_name razor-agents
%define module_name_major Razor2
%define module_package_name razor-agents
#still unused: %define module_name_minor null


%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEperl-%{module_package_name}
IPS_Package_Name:	library/perl-5/razor-agents
Summary:                 %{module_name}-%{module_version} PERL module
License:                 Artistic 2.0
SUNW_Copyright:          perl-razor-agents.copyright
Version:                 %{perl_version}.%{module_version}
Source:                  http://downloads.sourceforge.net/razor/razor-agents-%{module_version}.tar.bz2
Group:		Development/Perl
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
%setup -q            -c -n %name-%version
cd %{module_name}-%{module_version}

%build




cd %{module_name}-%{module_version}
perl Makefile.PL \
    UNINST=0 \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \

#make CC=$CC CCCDLFLAGS="                %picflags" OPTIMIZE="             %optflags" LD=$CC
make  CC=$CC CCCDLFLAGS="%{gnu_lib_path} %picflags" OPTIMIZE="-I%{gnu_inc} %optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version}
make install

#no idea why this is in the wrong place, so move it
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/%{perl_path_vendor_perl_version}/
mv  $RPM_BUILD_ROOT/%{_prefix}/lib/%{perl_dir}    $RPM_BUILD_ROOT/%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}
rm -r $RPM_BUILD_ROOT/%{_prefix}/lib

#remove: perllocal.pod
rm -r $RPM_BUILD_ROOT/%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/%{perl_dir}
#remove: .packlist
rm -r $RPM_BUILD_ROOT/%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/auto/%{module_package_name}


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/%{module_name_major}
%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/%{module_name_major}/*
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/auto
%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/auto/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

#special case because package delivers regular binary to non perl localtion  and has non-perl manpages
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- take care of special moving around of mis-layed directories (as well now with parametrized perl location/version)
* Tue Feb  1 2011 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWsfwhea}, %include packagenamemacros.inc
* Sun Mai 03 2009  - Thomas Wagner
- initial spec
