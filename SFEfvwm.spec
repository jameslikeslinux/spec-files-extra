#
# spec file for package SFEfvwm.spec
#
# includes module(s): fvwm
#
%include Solaris.inc

%include base.inc
%use fvwm = fvwm.spec
%define _pkg_docdir %_docdir/fvwm

Name:                   SFEfvwm
Summary:                %{fvwm.summary}
License:                GPLv2
SUNW_Copyright:         fvwm.copyright
Version:                %{fvwm.version}
Source1:		Fvwm.desktop
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnu-readline
Requires: SUNWfontconfig
Requires: SUNWxwxft
Requires: SUNWxwplt
Requires: SUNWxwice
Requires: SUNWlibms
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWlibrsvg
BuildRequires: SUNWlibrsvg-devel
Requires: SUNWglib2
BuildRequires: SUNWglib2-devel
Requires: SUNWcairo
BuildRequires: SUNWcairo-devel
Requires: SUNWfreetype2
Requires: SUNWlexpt
Requires: SUNWlibcroco
BuildRequires: SUNWlibcroco-devel
Requires: SUNWgtk2
BuildRequires: SUNWgtk2-devel
Requires: SUNWlxml
BuildRequires: SUNWlxml-devel
Requires: SUNWpango
BuildRequires: SUNWpango-devel
Requires: SUNWpixman
Requires: SUNWbzip
BuildRequires: SUNWgnome-common-devel
Requires: SFElibstroke
BuildRequires: SFElibstroke-devel
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%fvwm.prep -d %name-%version/%{base_arch}

%build
%fvwm.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%fvwm.install -d %name-%version/%{base_arch}
(
  cd %name-%version/%base_arch/fvwm-%version
  cp AUTHORS ChangeLog COPYING NEWS README %buildroot/%_pkg_docdir
)
(
  cd $RPM_BUILD_ROOT%{_datadir}/locale
  mv sv_SE sv
  ln -s sv sv_SE
)

%if %build_l10n
%else
rm -rf %{buildroot}%{_datadir}/locale
%endif

mkdir -p %{buildroot}%{_datadir}/xsessions && cp %{SOURCE1} %{buildroot}%{_datadir}/xsessions/

%clean
rm -rf $RPM_BUILD_ROOT

%files
#%define _pkg_docdir %_docdir/fvwm
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
#%%doc -d %base_arch/fvwm-%version AUTHORS ChangeLog COPYING NEWS README
#%_docdir/commands
#%_docdir/fvwm
#%_docdir/images/
#%_docdir/modules/
%{_mandir}
%{_datadir}/fvwm
%{_datadir}/xsessions/Fvwm.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Aug 15 2011 - Knut Anders Hatlen
- Added missing build dependency
* Fri Aug 12 2011 - Knut Anders Hatlen
- Fix directory permissions
- Update dependencies
* Thu Jul 28 2011 - Alex Viskovatoff
- Add SUNW_Copyright and some files that are placed in %_pkg_doc_dir
* Mon Jul 11 2011 - Milan Jurik
- fix packaging
- add dm session
* Jul 2009 - dauphin@enst.fr
- SUNWreadline is in B117
* Fri Apr 27 2006 - dougs@truemail.co.th
- Initial version
