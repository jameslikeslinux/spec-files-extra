#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libwebp_64 = libwebp.spec
%endif

%include base.inc
%use libwebp = libwebp.spec

Name:		SFElibwebp
IPS_Package_Name:	image/library/libwebp
Version:	%{libwebp.version}
Summary:	WebP library
URL:		https://code.google.com/speed/webp/
Group:		System/Multimedia Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
WebP is a new image format that provides lossless and lossy compression for images on the web. 

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%libwebp_64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%libwebp.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%libwebp_64.build -d %name-%version/%_arch64
%endif

%libwebp.build -d %name-%version/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%libwebp_64.install -d %name-%version/%_arch64
%endif

%libwebp.install -d %name-%version/%{base_arch}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%_libdir/lib*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/*.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%{_includedir}

%changelog
* Wed Dec 28 2011 - Milan Jurik
- initial spec
