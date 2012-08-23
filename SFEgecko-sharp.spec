#
# spec file for package SFEgecko-sharp
#
# includes module(s): gecko-sharp
#
%include Solaris.inc

Name:         SFEgecko-sharp
IPS_Package_Name:	library/mono/gecko-sharp-2
License:      Other
Group:        System/Libraries
Version:      2.0-0.13
IPS_Component_Version:	0.13
Summary:      gtk# - .NET bindings for gecko
Source:       http://go-mono.com/sources/gecko-sharp2/gecko-sharp-%{version}.tar.bz2
URL:          http://www.mono-project.org/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc

BuildRequires: SUNWgnome-base-libs
BuildRequires: SFEmono-devel
#BuildRequires: SFEmonodoc
Requires: SUNWgnome-base-libs
Requires: SFEmono

%prep
%setup -q -n gecko-sharp-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, bin) %dir %{_libdir}/mono
%{_libdir}/mono/*
%dir %attr (0755, root, bin) %dir %{_libdir}/monodoc
%{_libdir}/monodoc/*
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Sep 16 2011 - jchoi42@pha.jhu.edu
- Bump to 2.0-0.13
* Sun Sep 02 2007 - trisk@acm.jhu.edu
- Update dependencies
* Sat Mar 17 2007 - laca@sun.com
- Initial spec
