#
# spec file for package SFEwxwidgets-gnu
#
# includes module(s): wxWidgets
#

#%define _basedir /usr/g++
%include Solaris.inc
%include packagenamemacros.inc
%include usr-g++.inc
%define cc_is_gcc 1
%include base.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use wxwidgets_64 = wxwidgets.spec
%endif

%include base.inc
%use wxwidgets = wxwidgets.spec



Name:                    SFEwxwidgets-gpp
IPS_Package_Name:	 library/graphics/g++/wxwidgets
Summary:                 %{wxwidgets.summary} (g++)
Group:                   Desktop (GNOME)/Libraries
URL:                     http://wxwidgets.org/
License:                 wxWidgets
SUNW_Copyright:          wxwidgets.copyright
Version:		 %{wxwidgets.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-libs
Requires:      SUNWgnome-vfs
Requires:      %{pnm_requires_SUNWlibsdl}
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
%ifarch i386 amd64
BuildRequires: SUNWxorg-mesa
%endif
BuildRequires: %{pnm_buildrequires_SUNWlibsdl_devel}
BuildRequires: SFEgcc
Requires:      SFEgccruntime


%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}

%ifarch amd64 sparcv9
mkdir %{name}-%{version}/%{_arch64}
%wxwidgets_64.prep -d %{name}-%{version}/%{_arch64}
%endif

mkdir %{name}-%{version}/%{base_arch}
%wxwidgets.prep -d %{name}-%{version}/%{base_arch}



%build
export CC=gcc
export CXX=g++
%ifarch amd64 sparcv9
%wxwidgets_64.build -d %name-%version/%_arch64
%endif

%wxwidgets.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%wxwidgets_64.install -d %name-%version/%_arch64
%endif

%wxwidgets.install -d %name-%version/%{base_arch}


%clean
rm -rf %{name}-%{version}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/wx*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%{_libdir}/wx

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/wx*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*
%{_libdir}/%{_arch64}/wx*
%endif
 
%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/bakefile
%dir %attr(0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/bakefile/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Jun 29 2012 - Thomas Wagner
- rework 32/64-bit build system, make -gpp and -gnu spec file similar
- Bump to 2.8.12
- add IPS_package_name with /gnu/ to show up it lives in /usr/gnu/ prefix
- add Group:
- remove option to use gnu-ld, always use solaris ld
- change to (Build)Requires to %{pnm_buildrequires_SUNWsdl_devel}, %include packagenamacros.inc
* Thu Jun 21 2009 - brian.cameron@sun.com
- Bump to 2.8.10.  Remove upstream ptach wxwidgets-02-fixcompile.diff.
* Fri Jun 29 2012 - Thomas Wagner
- bump to 2.8.12
- %use usr-g++.inc
* Mon Apr 16 2012 - Logan Bruns <logan@gedanken.org>
- Enabled xml (--use-expat) and added IPS package name.
* Mon Jul 18 2011 - Alex Viskovatoff
- Add -fpermissive flag to enable building with gcc 4.6
* Thu Jun 23 2011 - Alex Viskovatoff
- Fork SFEwxwidgets-gpp.spec off SFEwxwidgets-gnu.spec,
  using /usr/g++ as _basedir
- Bump to 2.8.12, removing obsolete wxwidgets-02-Tmacro.diff
- Don't build 64 bit libs, since the build fails with current SFEgcc,
  which we add to Requires
* Thu Jun 21 2009 - brian.cameron@sun.com
- Bump to 2.8.10.  Remove upstream patch wxwidgets-02-fixcompile.diff.
  Add patch wxwidgets-02-Tmacro.diff to resolve compile issue when building
  with the latest Sun Studio patches.
* Tue Sep 02 2008 - halton.huo@sun.com
- Bump to 2.8.8
- Add patch fixcompile.diff (copy from SFEwxwidgets.spec)
* Thu Feb 21 2008 - trisk@acm.jhu.edu
- Bump to 2.8.7
- Add SFEsdl dependency, add --with-gnomevfs, fix building subdirs
* Sat Sep 22 2007 - dougs@truemail.co.th
- Modified for GNU ld with gcc
* Tue Sep 18 2007 - brian.cameron@sun.com
- Bump to 2.8.5.  Remove upstream patch wxwidgets-02-sqrt.diff.
* Wed Aug 15 2007 - dougs@truemail.co.th
- removed -pthreads from wx-config to stop it infecting other builds
* Sat Aug 11 2007 - trisk@acm.jhu.edu
- Bump to 2.8.4 for compatibility with SFEwxwidgets
- Use CC=gcc to be consistent and not confuse build system
* Sat Jul 14 2007 - dougs@truemail.co.th
- Converted from SFEwxwidgets.spec
