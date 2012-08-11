#
# spec file for package SFEicinga
#
# includes module(s): icinga
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%include packagenamemacros.inc

Name:		SFEicinga
Version:	1.7.1
Summary:	Host/service/network monitoring program (icinga)
Group:		Applications/System
License:	GPLv2
URL:		http://www.icinga.org/
Source:		%{sf_download}/icinga/%{version}/icinga-%{version}.tar.gz
Source1:	icinga.xml
#Patch1:		icinga-01-cc.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc


BuildRequires:	%{pnm_buildrequires_perl_default}
Requires: 	%{pnm_buildrequires_perl_default}

BuildRequires:	%{pnm_buildrequires_SUNWsndm_devel}
Requires:	%{pnm_requires_SUNWsndm}
BuildRequires:	SUNWjpg-devel
Requires:	SUNWjpg
BuildRequires:	SUNWgd2
Requires:	SUNWgd2
Requires:	%{pnm_requires_SUNWapch22}

Requires:	%{name}-common

%description
Icinga (fork of Nagios)

%package common
Group:		Applications/System
Summary:	Provides common directories, uid and gid among icinga-related packages
SUNW_BaseDir:	/

%description common
Provides common directories, uid and gid among icinga-related packages.


%package devel
Group:		Applications/System
Summary:	Provides include files that Nagios-related applications may compile against
Requires:	%{name}
SUNW_BaseDir:	%{_basedir}


%description devel
Nagios is a program that will monitor hosts and services on your
network. It has the ability to email or page you when a problem arises
and when a problem is resolved. Nagios is written in C and is
designed to run under Linux (and some other *NIX variants) as a
background process, intermittently running checks on various services
that you specify.

This package provides include files that Nagios-related applications
may compile against.


%prep
%setup -q -n icinga-%{version}

#%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%{optflags} -I%{_prefix}/%{perl_default_includedir}"
export LDFLAGS="%{_ldflags}"


# --enable-cgi-log enables cgi logging - experimental!!
#   --disable-statusmap     disables compilation of statusmap CGI
#   --disable-statuswrl     disables compilation of statuswrl (VRML) CGI
#   --enable-nanosleep      enables use of nanosleep (instead sleep) in event
#                           timing
#   --enable-event-broker   enables integration of event broker routines
#   --enable-state-based-escal-ranges
#                           enables state based escalation ranges - attention:
#                           interferes with mk_livestatus neb module
#   --enable-idoutils       enables database connectivity using idoutils
#   --enable-oracle         enables idoutils with ocilib and oracle
#   --enable-pgsql          !use libdbis pgsql support instead, libpq not yet
#                           implemented! enables idoutils with libpq and pgsql
#   --enable-embedded-perl  will enable embedded Perl interpreter
#   --enable-nagiosenv      expose Icinga Environment variables as NAGIOS_*)
#   --enable-ssl            enables native SSL support
# 
# Optional Packages:
#   --with-icinga-user=<user>
#                           sets user name to run icinga
#   --with-icinga-group=<grp>
#                           sets group name to run icinga
#   --with-command-user=<user>
#                           sets user name for command access
#   --with-command-group=<grp>
#                           sets group name for command access
#   --with-web-user=USER    username for web writable files (default www-data)
#   --with-web-group=GROUP  group for web writable files (default www-data)
#   --with-mail=<path_to_mail>
#                           sets path to equivalent program to mail
#   --with-httpd-conf=<path_to_conf>
#                           sets path to Apache conf.d directory
#   --with-checkresult-dir=<path>
#                           sets path to check results spool directory
#   --with-temp-dir=<path>  sets path to temp directory path where Icinga can
#                           create temp files for service/host check results
#   --with-temp-file=<filepath>
#                           sets path to an Icinga exclusive update temp file
#                           i.e. /tmp/icinga.tmp
#   --with-state-dir=<filepath>
#                           sets path to custom localstate dir e.g.
#                           /var/spool/icinga
#   --with-http-auth-file=<filepath>
#                           sets path to an Icinga HTTP auth file
#   --with-plugin-dir=<path>
#                           sets path to plugins directory path i.e.
#                           $prefix/libexec
#   --with-eventhandler-dir=<path>
#                           sets path to eventhandlers directory path i.e.
#                           $prefix/libexec/eventhandlers
#   --with-log-dir=<path>   sets path to logging directory
#   --with-cgi-log-dir=<path>
#                           sets path to cgi logging directory
#   --with-ext-cmd-file-dir=<path>
#                           sets path to external command file directory
#   --with-p1-file-dir=<path>
#                           sets path to embedded perl p1.pl directory
#   --with-init-dir=<path>  sets directory to place init script into
#   --with-lockfile=<path>  sets path and file name for lock file
#   --with-icinga-chkfile=<path>
#                           sets path and file name for icinga initscript error
#                           file
#   --with-ido2db-lockfile=<path>
#                           sets path and file name for ido2db lock file
#   --with-ido-sockfile=<path>
#                           sets path and file name for ido sock file
#   --with-idomod-tmpfile=<path>
#                           sets path and file name for idomod tmp file
#   --with-gd-lib=DIR       sets location of the gd library
#   --with-gd-inc=DIR       sets location of the gd include files
#   --with-cgiurl=<local-url>
#                           sets URL for cgi programs (do not use a trailing
#                           slash)
#   --with-htmurl=<local-url>
#                           sets URL for public html
#   --with-ido-instance-name=<instancename>
#                           sets instance_name for IDOUtils in idomod.cfg
#   --with-ocilib-lib=DIR   sets location of the ocilib library
#   --with-ocilib-inc=DIR   sets location of the ocilib include files,
#   --with-oracle-lib=DIR   sets location of the oracle library
#   --with-pgsql-lib=DIR    !use libdbis pgsql support instead, libpq not yet
#                           implemented! sets location of the pgsql library
#   --with-pgsql-inc=DIR    !use libdbis pgsql support instead, libpq not yet
#                           implemented! sets location of the pgsql include
#                           files,
#   --with-dbi-lib=DIR      sets location of the libdbi library
#   --with-dbi-inc=DIR      sets location of the libdbi include files,
#   --with-perlcache        turns on cacheing of internally compiled Perl
#                           scripts
#   --with-ssl=DIR          sets location of the SSL installation
#   --with-ssl-inc=DIR      sets location of the SSL include files
#   --with-ssl-lib=DIR      sets location of the SSL libraries
#   --with-kerberos-inc=DIR sets location of the Kerberos include files
# 
# Some influential environment variables:
#   CC          C compiler command
#   CFLAGS      C compiler flags
#   LDFLAGS     linker flags, e.g. -L<lib dir> if you have libraries in a
#               nonstandard directory <lib dir>
#   LIBS        libraries to pass to the linker, e.g. -l<library>
#   CPPFLAGS    (Objective) C/C++ preprocessor flags, e.g. -I<include dir> if
#               you have headers in a nonstandard directory <include dir>
#   CPP         C preprocessor



#
#*** Configuration summary for icinga-core 1.7.1 06-18-2012 ***:
#
# General Options:
# -------------------------
#        Icinga executable:  icinga
#        Icinga user/group:  icinga,icinga
#       Command user/group:  icinga,icinga
#        Apache user/group:  webservd,webservd
#            Embedded Perl:  yes, with caching
#             Event Broker:  yes
#           Build IDOUtils:  no
#        Install ${prefix}:  /usr/share/icinga
#                Lock file:  /var/run/icinga.pid
#                Temp file:  /tmp/icinga.tmp
#                 Chk file:  /var/log/icinga/icinga.chk
#           HTTP auth file:  /etc/icinga/htpasswd.users
#            Lib directory:  /usr/lib/icinga
#            Bin directory:  /usr/sbin
#         Plugin directory:  /usr/lib/icinga/plugins
#   Eventhandler directory:  /usr/lib/icinga/plugins/eventhandlers
#            Log directory:  /var/log/icinga
#   Check result directory:  /var/log/icinga/spool/checkresults
#           Temp directory:  /tmp
#          State directory:  /var/log/icinga
#   Ext Cmd file directory:  /var/log/icinga/rw
#           Init directory:  /etc/init.d
#  Apache conf.d directory:  /etc/apache2/2.2/conf.d
#             Mail program:  /usr/bin/mail
#                  Host OS:  solaris2.11
#       Environment Prefix:  ICINGA_
#
# Web Interface Options:
# ------------------------
#                 HTML URL:  http://localhost/icinga/
#                  CGI URL:  http://localhost/icinga/cgi-bin/
# Traceroute (used by WAP):  /usr/sbin/traceroute
#

./configure \
	--prefix=%{_datadir}/icinga \
	--exec-prefix=%{_localstatedir}/lib/icinga \
        --with-httpd-conf=%{_sysconfdir}/apache2/2.2/conf.d \
	--with-init-dir=%{_initrddir} \
	--with-cgiurl=/icinga/cgi-bin \
	--with-htmlurl=/icinga \
	--with-lockfile=%{_localstatedir}/run/icinga.pid \
	--libdir=%{_libdir}/icinga \
	--with-icinga-user=icinga \
	--with-icinga-group=icinga \
        --with-command-user=icinga \
        --with-command-group=icinga \
        --with-web-user=webservd \
        --with-web-group=webservd \
	--bindir=%{_sbindir} \
	--libexecdir=%{_libdir}/icinga/plugins \
	--sysconfdir=%{_sysconfdir}/icinga \
	--localstatedir=%{_localstatedir}/log/icinga \
	--datadir=%{_datadir}/icinga/html \
	--with-gd-lib=%{_libdir} \
	--with-gd-inc=%{_includedir}/gd2 \
	--enable-embedded-perl \
	--with-perlcache \
	--with-template-objects \
	--with-template-extinfo \
        --enable-idoutils

#  --with-htmlurl, --with-icinga-grp, --with-template-objects, --with-template-extinfo
# 
# *** Configuration summary for icinga-core 1.7.1 06-18-2012 ***:
# 
#  General Options:
#  -------------------------
#         Icinga executable:  icinga
#         Icinga user/group:  icinga,icinga
#        Command user/group:  icinga,icinga
#         Apache user/group:  nobody,nogroup
#             Embedded Perl:  yes, with caching
#              Event Broker:  yes
#            Build IDOUtils:  no
#         Install ${prefix}:  /usr/share/icinga
#                 Lock file:  /var/run/icinga.pid
#                 Temp file:  /tmp/icinga.tmp
#                  Chk file:  /var/log/icinga/icinga.chk
#            HTTP auth file:  /etc/icinga/htpasswd.users
#             Lib directory:  /usr/lib/icinga
#             Bin directory:  /usr/sbin
#          Plugin directory:  /usr/lib/icinga/plugins
#    Eventhandler directory:  /usr/lib/icinga/plugins/eventhandlers
#             Log directory:  /var/log/icinga
#    Check result directory:  /var/log/icinga/spool/checkresults
#            Temp directory:  /tmp
#           State directory:  /var/log/icinga
#    Ext Cmd file directory:  /var/log/icinga/rw
#            Init directory:  /etc/init.d
#   Apache conf.d directory:  /etc/apache2/2.2/conf.d
#              Mail program:  /usr/bin/mail
#                   Host OS:  solaris2.11
#        Environment Prefix:  ICINGA_
# 
#  Web Interface Options:
#  ------------------------
#                  HTML URL:  http://localhost/icinga/
#                   CGI URL:  http://localhost/icinga/cgi-bin/
#  Traceroute (used by WAP):  /usr/sbin/traceroute
# 
# 

gmake -j$CPUS all


%install
rm -rf %{buildroot}

install -d -m 0755 %{buildroot}%{_sysconfdir}/apache2/2.2/conf.d

make DESTDIR=%{buildroot} INIT_OPTS="" INSTALL_OPTS="" COMMAND_OPTS="" CGIDIR="%{_libdir}/icinga/cgi-bin" CFGDIR="%{_sysconfdir}/icinga" fullinstall

install -d -m 0755 %{buildroot}%{_sysconfdir}/icinga/objects
install -d -m 0755 %{buildroot}%{_sysconfdir}/icinga/private
install -d -m 0755 %{buildroot}%{_libdir}/icinga/plugins/eventhandlers
install -d -m 0775 %{buildroot}%{_includedir}/icinga
install -D -m 0644 include/locations.h %{buildroot}%{_includedir}/icinga/locations.h
install -d -m 0755 %{buildroot}%{_localstatedir}/spool/icinga

install -m 0644 sample-config/cgi.cfg %{buildroot}%{_sysconfdir}/icinga/cgi.cfg
install -m 0644 sample-config/mrtg.cfg %{buildroot}%{_sysconfdir}/icinga/mrtg.cfg
install -m 0644 sample-config/icinga.cfg %{buildroot}%{_sysconfdir}/icinga/icinga.cfg
install -m 0644 sample-config/resource.cfg %{buildroot}%{_sysconfdir}/icinga/resource.cfg
install -m 0644 sample-config/template-object/commands.cfg  %{buildroot}%{_sysconfdir}/icinga/objects/commands.cfg
install -m 0644 sample-config/template-object/contacts.cfg %{buildroot}%{_sysconfdir}/icinga/objects/contacts.cfg
install -m 0644 sample-config/template-object/localhost.cfg %{buildroot}%{_sysconfdir}/icinga/objects/localhost.cfg
install -m 0644 sample-config/template-object/printer.cfg %{buildroot}%{_sysconfdir}/icinga/objects/printer.cfg
install -m 0644 sample-config/template-object/switch.cfg %{buildroot}%{_sysconfdir}/icinga/objects/switch.cfg
install -m 0644 sample-config/template-object/templates.cfg %{buildroot}%{_sysconfdir}/icinga/objects/templates.cfg
install -m 0644 sample-config/template-object/timeperiods.cfg %{buildroot}%{_sysconfdir}/icinga/objects/timeperiods.cfg
install -m 0644 sample-config/template-object/windows.cfg %{buildroot}%{_sysconfdir}/icinga/objects/windows.cfg

install -d 0755 %{buildroot}%/var/svc/manifest/site
install -m 0644 %{SOURCE1} %{buildroot}%/var/svc/manifest/site

%clean
rm -rf %{buildroot}


%pre common
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/groupadd icinga';
  echo '/usr/sbin/useradd -d %{_localstatedir}/spool/icinga -s /bin/true -g icinga icinga';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun common
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel icinga';
  echo '/usr/sbin/groupdel icinga';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions
group groupname="icinga"
user ftpuser=false gcos-field="Nagios Reserved UID" username="icinga" password=NP group="icinga"
# need to add user webservd to icinga group

%files
%defattr(-, root, bin)
%doc Changelog INSTALLING LICENSE README UPGRADING
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
##TODO## this doesn't look right:    /usr/share/icinga/share/log
%{_datadir}/icinga/*
#TODO##%{_datadir}/icinga/html/robots.txt
#TODO##%{_datadir}/icinga/html/[^i]*
#TODO##%{_datadir}/icinga/html/contexthelp
#TODO##%{_datadir}/icinga/html/[^d]*
#TODO##%{_datadir}/icinga/html/[^m]*
#TODO##%{_datadir}/icinga/html/[^s]*
#TODO##%attr(0644, root, bin) %config(noreplace) %{_datadir}/icinga/html/config.inc.php
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
##TODO##%{_libdir}/icinga/cgi-bin/*cgi
%dir %attr(0755, root, bin) %{_libdir}/icinga/plugins
%dir %attr(0755, root, bin) %{_libdir}/icinga/plugins/eventhandlers

%files common
%defattr(-, root, sys)
##TODO##%{_initrddir}/icinga
%dir %attr(0755, root, bin) %{_sysconfdir}/apache2
%dir %attr(0755, root, bin) %{_sysconfdir}/apache2/2.2
%dir %attr(0755, root, bin) %{_sysconfdir}/apache2/2.2/conf.d
##TODO##%config(noreplace) %{_sysconfdir}/apache2/2.2/conf.d/icinga.conf
%dir %attr(0750, root, icinga) %{_sysconfdir}/icinga
%config(noreplace) %{_sysconfdir}/icinga/*cfg
%dir %attr(0750, root, icinga) %{_sysconfdir}/icinga/objects
%config(noreplace) %{_sysconfdir}/icinga/objects/*cfg
%dir %attr(0750, root, icinga) %{_sysconfdir}/icinga/private
%dir %attr(0755, root, bin) %{_localstatedir}/spool
%dir %attr(0755, icinga, icinga) %{_localstatedir}/spool/icinga
##TODO##%dir %attr(0750, icinga, icinga) %{_localstatedir}/log/icinga
##TODO##%dir %attr(0750, icinga, icinga) %{_localstatedir}/log/icinga/archives
##TODO##%dir %attr(2775, icinga, icinga) %{_localstatedir}/log/icinga/rw
##TODO##%dir %attr(0750, icinga, icinga) %{_localstatedir}/log/icinga/spool/
##TODO##%dir %attr(0750, icinga,icinga) %{_localstatedir}/log/icinga/spool/checkresults
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/site
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/icinga.xml

%files devel
%defattr(-, root, bin)
%{_includedir}/icinga

%changelog

error: Installed (but unpackaged) file(s) found:
        /usr/share/icinga
        /usr/share/icinga/share
        /usr/share/icinga/share/log
pkgbuild: SFEicinga.spec(442): Installed (but unpackaged) file(s) found
kommandant tom ~/spec-files-extra

pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/etc/init.d/icinga
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/etc/apache2/2.2/conf.d/icinga.conf
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/var/log/icinga
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/var/log/icinga/archives
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/var/log/icinga/rw
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/var/log/icinga/spool
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/var/log/icinga/spool/checkresults
kommandant tom ~/spec-files-extra

## Packaging complete.
Creating packages...
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/usr/share/icinga/html/robots.txt
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/usr/share/icinga/html/[^i]*
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/usr/share/icinga/html/contexthelp
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/usr/share/icinga/html/[^d]*
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/usr/share/icinga/html/[^m]*
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/usr/share/icinga/html/[^s]*
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/usr/share/icinga/html/config.inc.php
pkgbuild: File not found by glob: /var/tmp/pkgbuild-tom/SFEicinga-1.7.1-build/usr/lib/icinga/cgi-bin/*cgi
ERROR: SFEicinga FAILED
Would you like to continue? (yes/no) [yes]
* Thu Aug  9 2012 - Thomas Wagner
- initial spec (copy of SFEnagios.spec
