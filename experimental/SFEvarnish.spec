##
# spec file for package: varnish
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

##TODO## make SMF manifest more nice, check for /etc/varnish.cfg present

%include Solaris.inc

%define src_name varnish

# /var/svc/manifest/..l1../..l2..
%define svcdirl1 application
%define svcdirl2 proxy

Name:           SFEvarnish
Summary:        The Pound program is a reverse proxy, load balancer and HTTPS front-end for Web server(s)
Version:        3.0.2
License:        FreeBSD
URL:            http://www.varnish-cache.org
Source:         http://repo.varnish-cache.org/source/varnish-%{version}.tar.gz
Source1:	%{src_name}-manifest.xml
Source2:	%{src_name}.cfg

# OpenSolaris IPS Manifest Fields
Meta(info.upstream): varnish-misc@varnish-cache.org
Meta(info.maintainer): tom68@users.sourceforge.net
Meta(info.classification): org.opensolaris.category.2008:Applications/Internet


BuildRoot:      %{_tmppath}/%{src_name}-%{version}-build
SUNW_Basedir:   /
SUNW_Copyright: %{src_name}.copyright


#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
BuildRequires: SFEgcc
Requires: SFEgccruntime
#BuildRequires: SUNWopenssl-include
#BuildRequires: SUNWbtool
#BuildRequires: SUNWggrp
#Requires: SUNWopensslr
#Requires: SUNWopenssl-libraries
#Requires: SUNWlibms
#Requires: SUNWpcre
#Requires: SUNWzlib
#Requires: SUNWbzip


%description
Varnish cache accellerates web applications by caching.
See the website %{URL} for all details.

%prep
%setup -q -n %{src_name}-%{version}


%build
#/usr/gnu/bin/gcc or /usr/gcc/bin/gcc
export CC=/usr/gnu/bin/gcc
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -lmtmalloc"
export CFLAGS="%{optflags} -I/usr/sfw/include -I/usr/include/pcre"

./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
	    --localstatedir=%{_localstatedir} \



%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#Install example config file
#cp "%{SOURCE2}" "${RPM_BUILD_ROOT}/etc/varnish.cfg.example"

#Install manifest
mkdir -p ${RPM_BUILD_ROOT}/%{_localstatedir}/svc/manifest/%{svcdirl1}/%{svcdirl2}
cp "%{SOURCE1}" "${RPM_BUILD_ROOT}/%{_localstatedir}/svc/manifest/%{svcdirl1}/%{svcdirl2}/%{src_name}.xml"

find ${RPM_BUILD_ROOT}/%{_prefix} -name \*la -exec rm {} \;


%clean
rm -rf %{buildroot}

%if %(test -f /usr/sadm/install/scripts/i.manifest && echo 0 || echo 1)
%iclass manifest -f i.manifest
%endif


%files
%defattr(-,root,sys)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*
%{_libdir}/varnish*
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*

%dir %attr(755,root,sys) /etc
#%config(noreplace) %attr(644,root,root) /etc/*
%{_sysconfdir}/*

%defattr(-,root,sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/%{src_name}
%class(manifest) %attr (0444, root, sys) %{_localstatedir}/svc/manifest/%{svcdirl1}/%{svcdirl2}



%changelog
* Fri Oct 28 2011 - Thomas Wagner
- initial version
