#
# spec libedit for package file
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libedit_64 = libedit.spec
%endif

%include base.inc
%use libedit = libedit.spec

%include packagenamemacros.inc

Name:		SFEeditline
IPS_package_name:	library/libedit
Summary:	%{libedit.summary}
Version:	%{libedit.version}
License:	%{libedit.license}
Url:		%{libedit.url}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright:	%{name}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

# OpenSolaris IPS Package Manifest Fields
Meta(info.maintainer):	 	taki@justplayer.com
Meta(info.upstream):	 	http://www.thrysoee.dk/editline/
# Meta(info.repository_url):	[open source code repository]
Meta(info.classification):	System Libraries

BuildRequires:	SUNWhea
BuildRequires:	SUNWcsl
Requires:	SUNWcsl

%description
This is an autotool- and libtoolized port of the NetBSD Editline library (libedit). This Berkeley-style licensed command line editor library provides generic line editing, history, and tokenization functions, similar to those found in GNU Readline.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libedit_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libedit.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libedit_64.build -d %name-%version/%_arch64
%endif

%libedit.build -d %name-%version/%{base_arch}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%libedit_64.install -d %name-%version/%_arch64
%endif

%libedit.install -d %name-%version/%{base_arch}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr(0755, root, other) %{_libdir}/pkgconfig
%dir %attr(0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/%{_arch64}/pkgconfig/*

%changelog
* Sat Jun 02 2012 - Milan Jurik
- better multiarch support
* Sun Jul 31 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- omit -fast option.
* Sun Jun  5 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Fix dependency using pnm.
* Sat Mar 26 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Change permissions.
* Tue Jan  5 JST 2010 TAKI, Yasushi <taki@justplayer.com>
- Initial Revision
