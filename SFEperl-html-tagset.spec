#
# spec file for package SFEperl-html_tagset
#
# includes module(s): HTML-Tagset perl module
#
# Copyright (c) 2008 Rafael Alfaro
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include packagenamemacros.inc

%define html_tagset_version 3.20 

Name:                    SFEperl-html-tagset
IPS_Package_Name:	library/perl-5/html-tagset
Summary:                 HTML-%{html_tagset_version} PERL module
Version:                 %{perl_version}.%{html_tagset_version}
Source:                  http://www.cpan.org/modules/by-module/HTML/HTML-Tagset-%{html_tagset_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
Group:                   Development
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           %{pnm_buildrequires_perl_default}
Requires:                %{pnm_requires_perl_default}

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build
cd HTML-Tagset-%{html_tagset_version}
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd HTML-Tagset-%{html_tagset_version}
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

#remove %{perl_version}/%{perl_dir} ###/auto/.packlist
rm -rf $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/HTML
%{_prefix}/%{perl_path_vendor_perl_version}/HTML/*.pm
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- note: INSTALLSITELIB now without the directory %{perl_dir} (platform specific directory)
- remove /auto/.packlist
* Tue Feb  1 2011 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWsfwhea}, %include packagenamemacros.inc
* Sat Aug 17 2008 - rafael.alfaro@gmail.com
- Add license and group
* Thu Jun 19 2008 - rafael.alfaro@gmail.com
- Initial spec file 
