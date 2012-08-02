#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc
%define cc_is_gcc 1
%define _prefix %_basedir/g++

%ifarch amd64 sparcv9
%include arch64.inc
%use libwpd_64 = libwpd.spec
%endif

%include base.inc
%use libwpd = libwpd.spec

Name:		SFElibwpd-gpp
IPS_Package_Name:	text/library/g++/libwpd
License:	LGPL
Summary:	A library for import/export to WordPerfect files.
Version:	%{libwpd.version}
URL:		http://libwpd.sourceforge.net/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWgnome-base-libs
BuildRequires:	SUNWgnome-base-libs-devel

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%libwpd_64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%libwpd.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%libwpd_64.build -d %name-%version/%_arch64
%endif

%libwpd.build -d %name-%version/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%libwpd_64.install -d %name-%version/%_arch64
%endif

%libwpd.install -d %name-%version/%{base_arch}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Thu Dec 29 2011 - Milan Jurik
- bump to 0.9.4, rename to libwpd, use GCC for g++ ABI
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Initial spec.
