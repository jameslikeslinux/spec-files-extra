#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define osbuild %(uname -v | sed -e 's/[A-z_]//g')

%define python_version 2.6

%define src_name exo
%define src_url http://archive.xfce.org/xfce/4.8/src/

Name:		SFElibexo
Summary:	Application library for the Xfce desktop environment
Version:	0.6.0
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:	SFExfce4-dev-tools
BuildRequires:	SFElibxfce4util-devel
Requires:	SFElibxfce4util
Requires:	SFExfconf
Requires:	SFEperl-uri
BuildRequires:	SFEperl-uri
Requires:	SUNWgnome-panel
BuildRequires:	SUNWgnome-panel-devel
BuildRequires:	SUNWlxsl

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%package devel
Summary:	%{summary} - developer files
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

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
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export PYTHON=%/usr/bin/python%{python_version}

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lpython%{python_version}"
./configure --prefix=%{_prefix}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-gtk-doc		\
	--enable-xsltproc		\
	--disable-static		\
	--enable-python

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete libtool .la files
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

# move python stuff to vendor-packages
(
  cd $RPM_BUILD_ROOT%{_libdir}/python*
  mv site-packages vendor-packages
)

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}
%{_libdir}/lib*.so*
%{_libdir}/xfce4/exo-1/exo-compose-mail-1
%{_libdir}/xfce4/exo-1/exo-helper-1
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%{_libdir}/python%{python_version}/*
%if %(expr %{osbuild} '<' 165)
%{_libdir}/gio/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/exo-open.*
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_datadir}/xfce4
%dir %attr (0755, root, bin) %{_datadir}/pygtk
%{_datadir}/xfce4/*
%{_datadir}/pygtk/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/exo

%files root
%defattr(-, root, sys)
%{_sysconfdir}/xdg

%files devel
%defattr(-, root, bin)
%{_bindir}/exo-csource
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/exo-csource.*
%{_datadir}/gtk-doc/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Mar 21 2011 - Milan Jurik
- bump to 4.8.0, move to SFE from osol xfce
* Wed Aug 04 2010 - brian.cameron@oracle.com
- Fix packaging after updating to new version.
* Wed Aug 19 2009 - sobotkap@gmail.com
- Added IPS meta-tags required by juicer.
* Thu Aug 13 2009 - sobotkap@gmail.com
- Added include file xfce.inc.
* Sun Mar 01 2009 - sobotkap@gmail.com
- Bump to version 0.3.100 and clean %files section
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
- add hack that decides whether to depend on SUNWgnome-panel or OSOLlibnotify
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added another fixgccism patch
* Fri Feb  9 2007 - dougs@truemail.co.th
- Added libnotify and change perl-ui requirement - Copied from SFE repository
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
