#
# spec file for package SFEossp-uuid
#
# includes module(s): ossp-uuid
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use ossp_uuid_64 = ossp-uuid.spec
%endif

%include base.inc
%use ossp_uuid = ossp-uuid.spec

Name:                    SFEossp-uuid
IPS_package_name:        library/ossp-uuid
Summary:                 %{ossp_uuid.summary}
Version:                 %{ossp_uuid.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%ossp_uuid_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%ossp_uuid.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%ossp_uuid_64.build -d %name-%version/%_arch64
%endif

%ossp_uuid.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%ossp_uuid_64.install -d %name-%version/%_arch64
%endif

%ossp_uuid.install -d %name-%version/%{base_arch}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/uuid
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/uuid-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Thu May 12 2011 - Albert Lee <trisk@opensolaris.org>
- Initial sepc
