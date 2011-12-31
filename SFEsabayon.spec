#
# spec file for package sabayon
#
# Copyright (c) 2010 Sun Microsystems, Inc.
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby 
#
%include Solaris.inc
%include default-depend.inc

%define python_version 2.6
%define	src_name sabayon

Name:		SFEsabayon
IPS_Package_Name:	desktop/sabayon
Summary:	Tool to maintain user profiles in a GNOME desktop
Version:	2.30.1
Release:	1
Distribution:	Java Desktop System
Vendor:		Gnome Community
License:	GPLv2+
Group:		Applications/System
Source0:	http://ftp.gnome.org/pub/GNOME/sources/sabayon/2.30/%{src_name}-%{version}.tar.bz2
URL:		http://www.gnome.org/projects/sabayon
SUNW_BaseDir:   %{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Sabayon is a tool to help sysadmins and user change and maintain the
default behaviour of the GNOME desktop.

%package admin
%include default-depend.inc
SUNW_BaseDir:   %{_basedir} 
Summary:	Graphical tools for Sabayon profile management
Group:		Applications/System

##OSOL Requres
BuildRequires:  SUNWpython26-xdg
Requires:       SUNWpython26-xdg
Requires:       SFEpessulus
Requires:       SUNWgnome-python-libs
Requires:       SUNWgnome-python26-libs
BuildRequires:  x11/server/xephyr
Requires:       x11/server/xephyr

%description admin
The sabayon-admin package contains the graphical tools which a
sysadmin should use to manage Sabayon profiles.

%package root
Summary:	%{summary} - / filesystem components
SUNW_BaseDir:	/
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

intltoolize --copy --force --automake
libtoolize --force
aclocal 

automake -a -c -f
autoconf

./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --libexecdir=%{_libdir}		\
	    --localstatedir=%{_localstatedir}   \
	    --mandir=%{_mandir}			\
	    --with-distro=debian

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2

make install  DESTDIR=$RPM_BUILD_ROOT

echo 'include "$(HOME)/.gconf.path.defaults"'  > $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/local-defaults.path
echo 'include "$(HOME)/.gconf.path.mandatory"' > $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/local-mandatory.path

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
   rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

   find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
   find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
   find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'
   find $RPM_BUILD_ROOT -type f -name "*.pyc" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre admin
groupadd -g 225 sabayon
useradd -u 225 -d %{_datadir}/empty -c "Sabayon user" -g sabayon sabayon

%post admin
%restart_fmri desktop-mime-cache gconf-cache

%postun admin
%restart_fmri desktop-mime-cache gconf-cache

if [ "$1" -eq 0 ]; then
	userdel sabayon
	groupdel sabayon
fi

%files 
%defattr(-, root, bin)
%doc AUTHORS ChangeLog NEWS README TODO ISSUES sabayon.schema
%{_sbindir}/sabayon-apply

%files admin
%defattr(-, root, bin)
%{_bindir}/sabayon
%{_libdir}/sabayon-session
%{_libdir}/python%{python_version}/vendor-packages/sabayon/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %{_datadir}/%{src_name}
%{_datadir}/applications/*
%{_mandir}
%{_datadir}/%{src_name}/ui/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%doc %{_datadir}/gnome/help/sabayon/*
%doc %{_datadir}/omf/sabayon/* 

%files root
%defattr(-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%config(noreplace) %{_sysconfdir}/gconf/2/local-defaults.path
%config(noreplace) %{_sysconfdir}/gconf/2/local-mandatory.path
%{_sysconfdir}/sabayon

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Dec 31 2011 - Milan Jurik
- fix packaging
* Fri Apr 22 2011 - Alex Viskovatoff
- Bump to 2.30.1; add missing dependencies
* Mon Jul 12 2010 - <yuntong.jin@sun.com>
- Init spec file

