#
# spec file for package SFEperl-LWP
#
# includes module(s): LWP
#

# Note: Sourcefile does not follow standard naming

%define module_version 6.4
%define module_version_download 6.04
%define module_name libwww-perl
%define module_name_major LWP
%define module_package_name libwww-perl

%include Solaris.inc
%include packagenamemacros.inc

Name:		SFEperl-lwp
IPS_Package_Name:	library/perl-5/libwww-perl-lwp
Summary:	%{module_name}-%{module_version} PERL module
Version:	%{perl_version}.%{module_version}
Source:		http://www.cpan.org/modules/by-module/%{module_name_major}/%{module_name}-%{module_version_download}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:	%{pnm_requires_perl_default}
BuildRequires:	%{pnm_buildrequires_perl_default}
BuildRequires:	SFEperl-compress-zlib
Requires:	SFEperl-compress-zlib
BuildRequires:	SFEperl-html-parser
Requires:	SFEperl-html-parser
BuildRequires:	SFEperl-uri
Requires:	SFEperl-uri

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build

cd %{module_name}-%{module_version_download}
perl Makefile.PL \
     -n \
    UNINST=0 \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \

make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version_download}
make install


#remove: /usr/lib/i86pc-solaris-64int/perllocal.pod
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%{_prefix}/perl5/vendor_perl/%{perl_version}/*
#%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{module_name_major}
#%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/%{module_name_major}
#%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/%{module_name_major}/*
#%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto
#%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*



%changelog
* Sun May 27 2012 - Milan Jurik
- bump to 6.04, all except LWP:: went to separate packages
* Tue Feb  1 2011 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWsfwhea}, %include packagenamemacros.inc
* Sun Jul 19 2009 - matt@greenviolet.net
- bumped verion to 5.829
- Added missing Requires
* Wed Nov 28 2007 - Thomas Wagner
- renamed package and if necessary (Build-)Requires
* Sat Nov 24 2007 - Thomas Wagner
- moved from site_perl to vendor_perl
- released into the wild
* Wed, 19 July 2007  - Thomas Wagner
- Initial spec file
