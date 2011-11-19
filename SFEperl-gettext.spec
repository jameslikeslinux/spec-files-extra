#
# spec file for package SFEperl-gettext
#
# includes module(s): Gettext perl module
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include packagenamemacros.inc

Name:		SFEperl-gettext
IPS_Package_Name:	library/perl-5/gettext
Summary:	Gettext-%{gettext_version} PERL module
Version:	1.05
IPS_Component_Version:	1.5
Source:		http://www.cpan.org/modules/by-module/Locale/gettext-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc

%prep
%setup -q -n gettext-%version

%build
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
make install

#mkdir -p $RPM_BUILD_ROOT%{_prefix}/perl5
#mv $RPM_BUILD_ROOT%{_prefix}/lib/site_perl $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl
#mv $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/Image $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}
#mv $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/auto/Image/Size/* $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/Image/Size/
#rm -rf $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/auto
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

#mkdir -p $RPM_BUILD_ROOT%{_datadir}
#mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_mandir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Sat Nov 19 2011 - Milan Jurik
- add IPS package name, cleanup
* Sun Apr 11 2010 - Milan Jurik
- added missing build dependency
* Tue Mar 24 2009 - andras.barna@gmail.com
- IPSize version
* Wed Sep 12 2007 - nonsea@users.sourceforge.net
- Initial spec
