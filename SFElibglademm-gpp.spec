#
# spec file for package SFElibglademm
#
# includes module(s): libglademm
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define _prefix /usr/g++

Name:                    SFElibglademm-gpp
IPS_Package_Name:	library/desktop/g++/libglademm
Summary:                 C++ Wrapper for the glade Gnome UI designer (g++ built)
Group:                   Desktop (GNOME)/Libraries
Version:                 2.6.7
URL:                     http://www.gtkmm.org/
Source:                  http://ftp.acc.umu.se/pub/GNOME/sources/libglademm/2.6/libglademm-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: developer/ui-designer/glade
Requires: SFEglibmm-gpp
Requires: SFEcairomm-gpp
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SUNWsigcpp
Requires: SUNWlibC
Requires: SFEgtkmm-gpp
BuildRequires: developer/ui-designer/glade
BuildRequires: SFEsigcpp-gpp-devel
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:                 libglademm - C++ Wrapper for glade - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SUNWglibmm-devel
Requires: SUNWsigcpp-devel


%prep
%setup -q -n libglademm-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="-L/usr/g++/lib -R/usr/g++/lib"
export PKG_CONFIG_PATH="/usr/g++/lib/pkgconfig"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-python

# prevent useless extra_defs_gen from being built
sed -i 's/tools//' Makefile

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_datadir}/devhelp
#mv $RPM_BUILD_ROOT%{_bindir}/demo $RPM_BUILD_ROOT%{_bindir}/libglademm-demo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Aug 29 2011 - Alex Viskovatoff
- Fork new spec off SFElibglademm.spec
* Thu Oct 08 2009 - jchoi42@pha.jhu.edu
- Bump to 2.6.7, prevent useless extra_defs_gen from being built
- Add patch to prevent building useless extra_defs_gen
* Wed Sep 19 2007 - trisk@acm.jhu.edu
- Bump to 2.6.4
* Jun 05 2007 Thomas Wagner
- needed by pulseaudio frontends
- initial version from the museeum of spec-files (copy of SFEgtkmm.spec)
