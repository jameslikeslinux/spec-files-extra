#
# spec file for package SFEbdb
#
# includes module(s): bdb
#
%include Solaris.inc

#SUNWbdb is w/o db.h, we install in /usr/gnu/
%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use bdb_64 = bdb.spec
%endif

%include base.inc
%use bdb = bdb.spec

Name:		SFEbdb
IPS_Package_Name:	sfe/database/bdb
Summary:	%{bdb.summary}
Group:		%{bdb.group}
Version:	%{bdb.version}
License:        %{bdb.license}
SUNW_Copyright: bdb.copyright
URL:		%{bdb.url}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%bdb_64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%bdb.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%bdb_64.build -d %name-%version/%_arch64
%endif

%bdb.build -d %name-%version/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%bdb_64.install -d %name-%version/%_arch64
%endif

%bdb.install -d %name-%version/%{base_arch}

mkdir -p %{buildroot}%{_bindir}/%{base_isa}
for i in `ls -1 %{buildroot}%{_bindir}/db_*`; do
  mv $i %{buildroot}%{_bindir}/%{base_isa}/
  cd %{buildroot}%{_bindir} && ln -s ../../lib/isaexec `basename $i`
done

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{base_isa}/db_*
%hard %{_bindir}/db_*
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/db_*
%endif
%else
%{_bindir}/db_*
%endif
%{_libdir}/libdb*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/libdb*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Tue Aug 28 2012 - Milan Jurik
- support multiarch
* Wed Mar 30 2011 - Milan Jurik
- bump to 4.8.30
* Thu Feb 03 2011 - Milan Jurik
- fix docdir group
* Fri Jan 29 2010 - brian.cameron@sun.com
- Bump to 4.8.26.
* Thr Apr 30 2009 - Thomas Wagner
- bump version to 4.7.25
- use usr-gnu.inc to avoid conflicts with SUNWbdb (which unfortunately doesn't provide db.h)
* Fri Jan 05 2007 - daymobrew@users.sourceforge.net
- Add URL.
* Tue Nov 07 2006 - glynn.foster@sun.com
- Initial spec file

