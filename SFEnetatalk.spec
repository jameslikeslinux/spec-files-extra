#
# spec file for package: netatalk
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# include module(s): 
#
%include Solaris.inc
%include packagenamemacros.inc

Name:           SFEnetatalk
IPS_package_name:       service/network/netatalk
Summary:        Open Source Apple Filing Protocol (AFP) fileserver
Group:		System/Services
Version:        2.2.3
License:        GLPv2
Source:         %{sf_download}/netatalk/netatalk-%{version}.tar.bz2
URL:            http://netatalk.sourceforge.net/
Group:          Network
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community

%include default-depend.inc

BuildRequires: SFEbdb
BuildRequires: %{pnm_buildrequires_SUNWlibgcrypt}
BuildRequires: %{pnm_buildrequires_SUNWopenssl}
BuildRequires: %{pnm_buildrequires_system_network_avahi}
BuildRequires: %{pnm_buildrequires_SUNWavahi_bridge_dsd}
BuildRequires: %{pnm_buildrequires_SUNWavahi_bridge_dsd_devel}
BuildRequires: %{pnm_buildrequires_avahi_bridge_dsd}
Requires: SFEbdb
Requires: %{pnm_requires_SUNWlibgcrypt}
Requires: %{pnm_requires_SUNWopenssl}
Requires: %{pnm_requires_system_network_avahi}
Requires: %{pnm_requires_SUNWavahi_bridge_dsd}
Requires: %{pnm_requires_avahi_bridge_dsd}

#make the root package to be installed first
Requires: %name-root

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright: netatalk.copyright

# OpenSolaris IPS Manifest Fields
Meta(info.upstream): http://netatalk.sourceforge.net/ 
Meta(info.repository_url): http://netatalk.cvs.sourceforge.net/viewvc/netatalk/netatalk/
Meta(info.maintainer): <netatalk-devel@lists.sourceforge.net>

%description
Netatalk is a freely-available, kernel level implementation of the AppleTalk Protocol Suite, originally for BSD-derived systems. A *NIX/*BSD system running netatalk is capable of serving many macintosh clients simultaneously as an AppleTalk router, AppleShare file server (AFP), *NIX/*BSD print server, and for accessing AppleTalk printers via Printer Access Protocol (PAP). Included are a number of minor printing and debugging utilities.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:		%{summary} - root filesystem files, /
SUNW_BaseDir:		/

%prep
rm -rf %name-%version
%setup -q -n netatalk-%{version}

%build
export CFLAGS="%optflags -xc99=all "
export LIBS="-R/usr/gnu/lib"
./configure --prefix=%{_prefix}                  \
            --bindir=%{_bindir}                  \
            --mandir=%{_mandir}                  \
            --infodir=%{_infodir}                \
            --libexecdir=%{_libexecdir}/netatalk \
            --sysconfdir=%{_sysconfdir}          \
            --with-uams-path=%{_libdir}/netatalk \
            --with-spooldir=%{_localstatedir}/spool/netatalk  \
            --disable-ddp                        \
            --with-pam \
            --with-bdb=/usr/gnu \
            --with-libgcrypt-dir=/usr \
            --with-ssl-dir=/usr \
            --enable-nfsv4acls

make

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
  DESTDIR=$RPM_BUILD_ROOT \
  MANDIR=$RPM_BUILD_ROOT%{_mandir}

ginstall -D -m 755 distrib/initscripts/rc.atalk.sysv $RPM_BUILD_ROOT%{_sysconfdir}/init.d/netatalk

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/spool/netatalk
rm -rf $RPM_BUILD_ROOT/var/tmp
rm -rf $RPM_BUILD_ROOT/usr/lib/security
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/netatalk/*.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/netatalk/*.la

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %name-%version

%files
%defattr(-,root,bin)
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/netatalk/*


%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/netatalk/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*


%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0755, root, sys) %dir %{_sysconfdir}/init.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netatalk/*
%{_sysconfdir}/init.d/netatalk
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/spool
%dir %{_localstatedir}/spool/netatalk


%changelog
* Mon Jul 23 2012 - Milan Jurik
- bump to 2.2.3
- fix rpath for /usr/gnu/lib
* Sun Jan 22 2012 - TAKI, Yasushi
- bump to 2.2.2.
- Add IPS_package_name service/network/netatalk like samba package.
- Add dependency libgcrypt and ssl dir for supporting TimeMachine for Mac OSX Lion.
* Mon Aug  1 2011 - Alex Viskovatoff
- add SUNW_Copyright
* Mon Aug  1 2011 - Thomas Wagner
- hard (Build)Requires SFEbdb (depdend resol. won't work with SUNWgnu_dbm)
- fix %files permissions for /var/spool
* Mon Aug  1 2011 - Thomas Wagner
- bump to 2.2.0 in a separate commit, this is first stable 2.2.x for early adopters
- fix %files
* Mon Aug  1 2011 - Thomas Wagner
- bump to 2.1.5
* Sat Mar 20 2011 - Thomas Wagner
- fix permissions by rewriting %files section
- remove static libs
- add -root package for config files
- change (Build)Requires to %{pnm_buildrequires_SUNWgnu_dbm}
* Sat Mar 12 2011 - Thomas Wagner
- mkdir -p spool directory (packaging error)
- remove typo in --with-bdb
- clean up SourceJucier dependencies: (Build)Requires  s/bdb/SFEbdb/
- add --with-bdb=/usr/gnu
* Tue Jun 29 2010 -  Michal Bielicki cypromis@opensolaris.org
- bumped up version to 2.1.2
- fixed some missing included
- fixed files
- added devel package
- created SFE version
- cleared some attributes
- added pam support
* Sun Apr 04 2010 - yabawock@gmail.com
- New upstream release
- Enable support for NFSv4 ACLs
* Wed Feb 17 2010 - sebastian.laubscher@interdose.com
- initial version
