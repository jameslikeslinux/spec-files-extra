#
# spec file for package SFEredshift
#
# includes module(s): redshift
#
%include Solaris.inc
%define python_version 2.6

Name:        redshift
IPS_package_name: desktop/redshift
SUNW_Pkg:    SFEredshift
Summary:     redshift color temperature adjustment utility
Version:     1.6
Release:     1
License:     GPLv3
Source:      http://launchpad.net/redshift/trunk/%{version}/+download/redshift-%{version}.tar.bz2
Patch01:     redshift-01-signal.h.diff
Patch02:     redshift-02-clock-applet.diff
Patch03:     redshift-03-gerror-leak.diff
#SUNW_Copyright: %{name}.copyright
BuildRoot:   %{_tmppath}/%{name}-%{version}-build
Requires: SUNWxorg-clientlibs
Requires: SUNWgtk2
Requires: SUNWPython26
%include default-depend.inc

%description
Redhift adjusts the color temperature of your screen according to your
surroundings. This may help your eyes hurt less if you are working in
front of the screen at night.

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%setup -q 
%patch1 -p1
%patch2 -p1
%patch3 -p1
# autoconf :(
ed -s configure.ac <<'/EOF/' >/dev/null
,s/2\.64/2\.63/
w
q
/EOF/

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

aclocal -I m4 $ACLOCAL_FLAGS
autoconf -f

export CFLAGS="%optflags"
./configure --prefix=%{_prefix}	\
	--bindir=%{_bindir}	\
	--datadir=%{_datadir}	\
	--libdir=%{_libdir}	\
	--enable-gnome-clock	\
	--enable-gui

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT%{_libdir}/python%{python_version}
mkdir -p vendor-packages/gtk_redshift
mv site-packages/gtk_redshift/* vendor-packages/gtk_redshift/
rmdir site-packages/gtk_redshift
rmdir site-packages
rm vendor-packages/gtk_redshift/*.pyo

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%clean
/bin/rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python2.6/vendor-packages/gtk_redshift
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Apr 25 2011 - Albert Lee <trisk@opensolaris.org>
- Bump to 1.6
- Support Studio
- Update patch1, add patch2, patch3 for GNOME clock support
* Tue Apr 20 2010 - laca@opensolaris.org
- create
