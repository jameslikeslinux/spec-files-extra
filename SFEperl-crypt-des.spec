#
# spec file for package SFEperl-crypt-des
#
# includes module(s): perl-crypt-des
#

%include Solaris.inc

%define tarball_version 2.05
%define source_name Crypt-DES

Name:                    SFEperl-crypt-des
Summary:                 %{source_name}-%{tarball_version} PERL Module
Version:                 %{perl_version}.%{tarball_version}
IPS_component_version:   2.5
Source:                  http://www.cpan.org/modules/by-module/Crypt/%{source_name}-%{tarball_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
%include perl-depend.inc

%prep
%setup -q	-c -n %name-%version
cd %{source_name}-%{tarball_version}

%build
cd %{source_name}-%{tarball_version}
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
cd %{source_name}-%{tarball_version}
make install

echo "DEBUG PRINT: "
find $RPM_BUILD_ROOT%{_prefix}/lib -ls
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*



%changelog
* Sat Aug  4 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- re-work build instructions
- use %include perl-depend.inc
- move out or perl/
* Tue Mar 02 2010 - matt@greenviolet.net
- Initial spec file
