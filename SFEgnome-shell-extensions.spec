#
# spec file for package SFEgnome-shell-extensions
#
# includes module(s): gnome-shell-extensions
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEgnome-shell-extensions
Summary:                 GNOME Shell
Version:                 3.1.3
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gnome-shell-extensions/3.1/gnome-shell-extensions-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWPython26-devel
BuildRequires:           SFEgnome-shell
Requires:                SFEgnome-shell
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gnome-shell-extensions-%version

%build

export PYTHON=/usr/bin/python%{pythonver}
automake-1.11 -a -c -f
autoconf
./configure \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --mandir=%{_mandir} \
   --sysconfdir=%{_sysconfdir}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache icon-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/glib-2.0
%{_datadir}/gnome-shell

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Jul 13 2011 - brian.cameron@oracle.com
- Created with version 3.1.3.
