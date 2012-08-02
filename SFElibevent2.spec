#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libevent2_64 = libevent2.spec
%endif

%include base.inc
%use libevent2 = libevent2.spec

Name:		SFElibevent2
IPS_Package_Name:	library/libevent2
Summary:	An event notification library for event-driven network servers.
License:	BSD
SUNW_Copyright:	libevent.copyright
Version:	%{libevent2.version}
URL:		http://monkey.org/~provos/libevent/
Group:		System/Libraries
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
%libevent2_64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%libevent2.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%libevent2_64.build -d %name-%version/%_arch64
%endif

%libevent2.build -d %name-%version/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%libevent2_64.install -d %name-%version/%_arch64
%endif

%libevent2.install -d %name-%version/%{base_arch}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}/event_rpcgen.py
%_libdir/lib*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif

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
* Thu Nov 17 2011 - Milan Jurik
- multiarch support
- IPS package name
- bump to 2.0.15
* Thu Aug 18 2011 - Alex Viskovatoff
- install in /usr/gnu so as not to conflict with system libevent; bump to 2.0.12
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Tue May 31 2011 - Alex Viskovatoff
- bump to 2.0.11
* Fri Mar 18 2011 - Alex Viskovatoff
- fork new spec off SFElibevent.spec
* Mon Mar 14 2011 - Alex Viskovatoff
- use %optflags
* Mon Jan 10 2011 - Thomas Wagner
- new download URL, original site currently down
* Wed May 13 2010 - Milan Jurik
- bump to 1.4.13
* Mon May 10 2010 - Milan Jurik
- update to 1.4.10
* Wed Feb 25 2009 - alfred.peng@sun.com
- Bump to 1.4.9 and build with Sun Studio.
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* DOW MMM DD 2006 - Eric Boutilier
- Initial spec
