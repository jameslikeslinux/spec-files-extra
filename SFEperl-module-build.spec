#
# spec file for package SFEperl-module-build
#
# includes module(s): Module-Build perl module
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include packagenamemacros.inc

#be carefull with this number upgrades only happen if the new package is numeric higher!
%define modulebuild_version 0.2808

Name:                    SFEperl-module-build
Summary:                 Module-Build-%{modulebuild_version} PERL module
Version:                 %{perl_version}.%{modulebuild_version}
Source:                  http://www.cpan.org/modules/by-module/Module/Module-Build-%{modulebuild_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           %{pnm_buildrequires_perl_default}
Requires:                %{pnm_requires_perl_default}
#BuildRequires:           SFEperl-extutils-cbuilder
#Requires:           SFEperl-extutils-cbuilder

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build
cd Module-Build-%{modulebuild_version}
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
cd Module-Build-%{modulebuild_version}
make install

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}
mv $RPM_BUILD_ROOT%{_prefix}/lib/site_perl/Module $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

#remove %{perl_version}/%{perl_dir} ###/auto/.packlist
rm -rf $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl}/%{perl_dir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_mandir} 

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/Module
%{_prefix}/%{perl_path_vendor_perl_version}/Module/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Thu Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- take care of special moving around of mis-layed directories (as well now with parametrized perl location/version)
- remove /auto/.packlist
* Wed Sep 12 2007 - nonsea@users.sourceforge.net
- Initial spec
