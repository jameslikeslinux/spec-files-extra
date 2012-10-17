#
# spec file for package: drupal6
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%include packagenamemacros.inc

%define     src_name drupal
%define     targetdirname drupal
#set to blank if not text part like ".RC2" is in the version string. IPS can't handle non-numeric version strings
#mind to include a "dot" if non empty
#%define     src_name_minor_extra 
%define     src_name_minor_extra 
%define     apache2_majorversion 2
%define     apache2_version 2.2
#IPS_component_version: <numeric-only>

Name:                SFEdrupal7
IPS_Package_Name:	 web/service/drupal 
Summary:             Drupal - open-source content-management platform
Version:             7.16
License: 	     GPLv2
Source:              http://ftp.drupal.org/files/projects/drupal-%{version}%{src_name_minor_extra}.tar.gz
#Source2:             %{src_name}-htaccess-protect-backend
Source3:             %{name}.conf.example
URL:	             http://www.drupal.org
Group:		Web Services/Portals
SUNW_BaseDir:        /
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}%{src_name_minor_extra}-build
%include default-depend.inc

Requires:            %{pnm_requires_SUNWapch22}
Requires:            %{pnm_requires_SUNWapch22m_php52}
Requires:            %{pnm_requires_SUNWphp52_mysql}
Requires:            %{pnm_requires_SUNWphp52}
Meta(info.upstream):            http://www.drupal.org/
Meta(info.maintainer):          Thomas Wagner <tom68@users.sourceforge.net>
Meta(info.classification):      org.opensolaris.category.2008:Social Applications

##TEMP## enhance description, drupal basics
%description
Drupal CMS System
see http://pkgbuild.wiki.sourcefore.net/SFEdrupal7.spec for initial setup 
instructions regarding Solaris (TM) and see www.drupal.org for
drupal platform independent instructions.
Note: Only english language files included. Please install more languages yourself.


%prep
%setup -q -n drupal-%version
#%setup -q -c -T -a0 -n %{src_name}-%{version}%{src_name_minor_extra}
#cp -p %{SOURCE2} .

#copy example apache config
cp -p %{SOURCE3} .

##[ -f .htaccess.default ] && mv .htaccess.default .htaccess
##[ -f ._htaccess ] && mv ._htaccess .htaccess

#%build

#dummy - nothing to make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/
#mv %{src_name}.conf.example $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{src_name}.conf
mv %{name}.conf.example $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{name}.conf

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
cp -pr * $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
#just in case we places an .htaccess or .htpasswd file here:
cp -pr .ht* $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
#mv %{src_name}-htaccess-protect-backend $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/.htaccess
ln -s %{src_name}-%{version}%{src_name_minor_extra} $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}

%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr (0640, webservd, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
     %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/*
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/.htaccess
#don't let wordpress modify it's files - for security owned by root and not writable by the webservd userid
#places explicitly needed writable are system/logs, system/html, system/tmp
%defattr (0644, root, bin)
#example %dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/writable_file_this_is

%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%class(renamenew) %{_sysconfdir}/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{name}.conf


%changelog
* Thu Oct 18 2012 - Thomas Wagner
- bump to 7.16 - DRUPAL-SA-CORE-2012-003 Security risk: Highly critical Exploitable from: Remote Vulnerability: Information Disclosure, Arbitrary PHP code execution
* Tue Sep 18 2012 - Thomas Wagner
- bump to 7.15 - bug fixes (no security fixes since 7.14)
* Sun May 06 2012 - Thomas Wagner
- bump to 7.14 - bug fixes + security fixes
* Thu Feb 23 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 7.12
* Fri Dec 30 2011 - Thomas Wagner
- bump to 7.10 - various fixes
* Fri Oct 31 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 7.9
* Fri Oct 14 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 7.8
* Sat Jul 30 2011 - Thomas Wagner
- bump to 7.7
* Sat Jul 16 2011 - Thomas Wagner
- bump to 7.4
* Sat Feb 12 2011 - Thomas Wagner
- initial version 7.0, derived form spec-files-jucr/specs/drupal6.spec
