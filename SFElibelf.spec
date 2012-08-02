#
# spec file for package SFElibelf
#
# includes module(s): libelf
#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc

%use libelf = libelf.spec

Name:		SFElibelf
IPS_Package_Name:	library/libelf
URL:		http://www.mr511.de/software/english.html
Summary:	libelf - A Library to Manipulate ELf Files
Version:	%{libelf.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - developer files
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}


%prep
rm -rf %name-%version
mkdir %name-%version
%libelf.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
%libelf.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libelf.install -d %name-%version

rm $RPM_BUILD_ROOT/usr/gnu/lib/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale/*

%files devel
%defattr (-, root, bin)
%{_includedir}/libelf

%changelog
* Fri Nov 25 2011 - Milan Jurik
- fix packaging
* Thu Feb 25 2010 - jchoi42@pha.jhu.edu
- Initial spec
