#pruefen, wo per default gesucht wird nach:  username map = /etc/gnu/samba/private/username.map
#pruefen, ob man die Logfiles alle nach /var/gnu/samba bringen kann
#exit 1

#
# spec file for package SFEsamba
#

%include Solaris.inc
#%define cc_is_gcc 1
#%define _gpp /usr/gnu/bin/g++
%include base.inc

#avoid clush with /usr/bin/profiles of SUNWcsu Solaris package
%include usr-gnu.inc

%define src_name samba

Name:                    SFEsamba
Summary:                 samba - CIFS Server and Domain Controller
URL:                     http://samba.org/
Version:                 3.5.18
Copyright:               GPL
Url:                     http://www.samba.org
Source:                  ftp://ftp.samba.org/pub/samba/stable/samba-%{version}.tar.gz
Source2:		sambagnu-smbd.xml
Source3:		sambagnu-nmbd.xml
Source4:		sambagnu-winbindd.xml
Source5:		addmachinescript-samba3
Source6:		domain-samba3.reg
Patch1:                 samba-01-oi-2172.diff
Patch6:                 samba-06-remove-attr_get-configure.in.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: Requirements 
BuildRequires: SUNWbash
BuildRequires: SFEgcc
Requires: SUNWbash
Requires: SFEgccruntime

%include default-depend.inc

%package swat
Summary:                 %{summary} - swat management web frontend
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package doc
Summary:                 %{summary} - documentation and manpages
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%description


%prep
%setup -q -n samba-%version

perl -w -pi.bak -e "s,^SHELL=/bin/sh,SHELL=/usr/bin/bash," source*/Makefile.in source*/Makefile
perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," `find source* -type f -exec grep -q "^#\!.*/bin/sh" {} \; -print`

#samba manifest
cp -p %{SOURCE2} sambagnu-smbd.xml
cp -p %{SOURCE3} sambagnu-nmbd.xml
cp -p %{SOURCE4} sambagnu-winbindd.xml
cp -p %{SOURCE5} addmachinescript
cp -p %{SOURCE6} domain.reg

#solaris useradd smb.conf.default
%patch6 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export SHELL=/usr/bin/bash

export CC="/usr/sfw/bin/gcc"
export CXX="/usr/sfw/bin/g++"

#compile time might have much never samba libs then the installed one on the disk
LIBSCOMPILETIME=`pwd`/nsswitch:`pwd`/source3/bin
export LD_LIBRARY_PATH=$LIBSCOMPILETIME

export CFLAGS="%optflags -L$LIBSCOMPILETIME -L/usr/gnu/lib/samba -L/usr/gnu/lib -R /usr/gnu/lib/samba -R/usr/gnu/lib -lncurses -ltermcap"
export CXXFLAGS="%cxx_optflags -L$LIBSCOMPILETIME -L/usr/gnu/lib/samba -L/usr/gnu/lib -R /usr/gnu/lib/samba -R/usr/gnu/lib"
export LDFLAGS="%_ldflags -L$LIBSCOMPILETIME -L/usr/gnu/lib/samba -L/usr/gnu/lib -R /usr/gnu/lib/samba -R/usr/gnu/lib"
export LDFLAGS="$LDFLAGS -lncurses -ltermcap"


cd source3
./autogen.sh
bash ./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --bindir=%{_bindir}         \
            --sbindir=%{_sbindir}         \
            --libdir=%{_libdir}/samba         \
            --libexecdir=%{_libexecdir}/samba \
            --sysconfdir=%{_sysconfdir}/samba \
	    --with-configdir=%{_sysconfdir}/samba \
	    --with-privatedir=%{_sysconfdir}/samba/private \
	    --sharedstatedir=%{_localstatedir}/samba \
	    --localstatedir=%{_localstatedir}/samba \
	    --datadir=%{_datadir} \
	    --with-swatdir=%{_datadir}/samba/swat \
            --enable-shared         \
            --enable-static=no      \
            --enable-fhs \
            --with-shared-modules=vfs_zfsacl,vfs_prealloc,vfs_cacheprime,vfs_commit,idmap_ldap,idmap_tdb2,idmap_rid,idmap_ad,idmap_hash,idmap_adex \
--with-aio-support \
--with-acl-support \
--with-ads \
--with-krb5 \
--with-ldap \
--with-automount \
--with-dnsupdate \
--with-pam \
            SHELL=/usr/bin/bash     \
            CFLAGS="$CFLAGS"        \
            CXXFLAGS="$CXXFLAGS"    \
            LDFLAGS="$LDFLAGS"      \
            CC="$CC"                \
            CXX="$CXX"              

#make
gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd source3
SHELL=/usr/bin/bash gmake install DESTDIR=$RPM_BUILD_ROOT
  	
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/samba/private
cp -p ../examples/smb.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/samba/

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log

# for older pkgbuild/pkgtool
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp ../sambagnu-smbd.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp ../sambagnu-nmbd.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp ../sambagnu-winbindd.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp ../addmachinescript ${RPM_BUILD_ROOT}%{_bindir}/
chmod a+rx  ${RPM_BUILD_ROOT}%{_bindir}/addmachinescript
[ -d ${RPM_BUILD_ROOT}%{_docdir}/%{name}/ ] || mkdir ${RPM_BUILD_ROOT}%{_docdir}/%{name}/
cp ../domain.reg ${RPM_BUILD_ROOT}%{_docdir}/%{name}/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc COPYING README README.Coding Read-Manifest-Now WHATSNEW.txt domain.reg
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/smbd
%{_sbindir}/nmbd
%{_sbindir}/winbindd
#swat see below
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
#for doc section from above
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%dir %attr (0755, root, other) %{_docdir}

#note manpage(s) swat included
%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files swat
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/swat
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/%{src_name}
%dir %attr (0755, root, bin) %{_datadir}/%{src_name}/swat
%{_datadir}/%{src_name}/swat/*


%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}/%{src_name}
%{_sysconfdir}/%{src_name}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/sambagnu-smbd.xml
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/sambagnu-nmbd.xml
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/sambagnu-winbindd.xml


%changelog
* Mon Oct 8 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 3.5.18
* Sat Sep 8 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 3.5.17
* Tue Apr 19 2011 - Thomas Wagner
- bump to 3.5.8
- new Download-URL
* Sun Mar 14 2010 - Thomas Wagner
- bump to 3.4.7
* Thr Nov 11 2009 - Thomas Wagner
- bump to 3.4.3, corrected download-URL
- add manifest for nmbd and winbindd, renamed manifest for smbd, new FMRI for samba and it's helper daemons, 3 in total
- add ext-sources addmachinescript to workaround "$" in machine-name to exit tools != 0 
* Thr Sep 24 2009 - Thomas Wagner
- bump / change series to version 3.4.1
* Thr Sep 24 2009 - Thomas Wagner
- bump to version 3.2.14  --- NOTE: seems to be discontinued
* Wed Jan  7 2009 - Thomas Wagner
- remove %post, %preun, %postun
- bump to version 3.2.7 to solve CVE-2009-0022 and CVE-2008-4314
- clean %doc, add mkdir %{_docdir} for compatibility to older pkgbuild/pkgtool
* Mon Oct 13 2008 - Thomas Wagner
- typo at mkdir for samba log
* Fri Oct 03 2008 - Thomas Wagner
- derive new SMF instance from samba.xml and add postinstall for import
* Sat Sep 13 2008 - Thomas Wagner
- Initial spec - derived from LSB/lsb-samba.spec


