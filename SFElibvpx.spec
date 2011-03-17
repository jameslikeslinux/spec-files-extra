#
# spec file for package SFElibvpx
#
# includes module(s): libvpx
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

# No sparcv9 target

%ifarch amd64
%include arch64.inc
%use libvpx_64 = libvpx.spec
%endif

%include base.inc
%use libvpx = libvpx.spec

Name:		SFElibvpx
Summary:	The VP8 Codec SDK
Group:		Libraries/Multimedia
Version:	%{libvpx.version}
URL:		http://www.webmproject.org/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SFEgcc
Requires: SFEgccruntime
BuildRequires: SFEyasm

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64
mkdir %name-%version/%_arch64
%libvpx_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libvpx.prep -d %name-%version/%{base_arch}

%build
export CC=/usr/gcc/4.5/bin/gcc

%ifarch amd64
%libvpx_64.build -d %name-%version/%_arch64
%endif

%libvpx.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64
%libvpx_64.install -d %name-%version/%_arch64
%endif

%libvpx.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Thu Mar 17 2011 - Milan Jurik
- initial spec
