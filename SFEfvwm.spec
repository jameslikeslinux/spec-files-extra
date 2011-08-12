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
Requires: SFElibstroke

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
* Fri Aug 12 2011 - Knut Anders Hatlen
- Fix directory permissions
* Thu Jul 28 2011 - Alex Viskovatoff
- Add SUNW_Copyright and some files that are placed in %_pkg_doc_dir
* Mon Jul 11 2011 - Milan Jurik
- fix packaging
- add dm session
* Jul 2009 - dauphin@enst.fr
- SUNWreadline is in B117
* Fri Apr 27 2006 - dougs@truemail.co.th
- Initial version
