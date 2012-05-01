# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use protobuf64 = protobuf.spec
%endif

%include base.inc
%use protobuf = protobuf.spec

Name:		SFEprotobuf
IPS_Package_Name:	library/protobuf
Summary:	%{protobuf.summary}
Version:	%{protobuf.version}
URL:		https://code.google.com/p/protobuf/
Group:		System/Libraries
License:	BSD
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
%include default-depend.inc

%description
Protocol Buffers are a way of encoding structured data in an efficient yet extensible format. Google uses Protocol Buffers for almost all of its internal RPC protocols and file formats.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version

%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%protobuf64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%protobuf.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%protobuf64.build -d %name-%version/%_arch64
%endif
    
%protobuf.build -d %name-%version/%base_arch

%install
rm -rf %{buildroot}

%ifarch amd64 sparcv9
%protobuf64.install  -d %name-%version/%_arch64
%endif
    
%protobuf.install -d %name-%version/%base_arch

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_bindir}
%{_libdir}/*.so*
%ifarch sparcv9 amd64
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch sparcv9 amd64
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Tue May 01 2012 - Milan Jurik
- Initial spec
