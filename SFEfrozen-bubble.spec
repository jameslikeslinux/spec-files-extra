#
# spec file for package SFEfrozen-bubble
#
# includes module(s): frozen-bubble
#
%include Solaris.inc
%include packagenamemacros.inc

Name:		SFEfrozen-bubble
IPS_Package_Name:	games/frozen-bubble
Summary:	Frozen Bubble - Colorful 3D rendered bubble shooting game
Version:	2.2.0
Source:		http://www.frozen-bubble.org/data/frozen-bubble-%{version}.tar.bz2
URL:		http://www.frozen-bubble.org

# owner:alfred date:2009-01-12 type:bug
Patch1:		frozen-bubble-01-build-sun-studio.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc

Requires:	SFEsdl-image
Requires:	SFEsdl-mixer
Requires:	SFEsdl-pango
Requires:	SFEsdl-perl
Requires:	SFEperl-gettext

BuildRequires:	SFEsdl-image-devel
BuildRequires:	SFEsdl-mixer-devel
BuildRequires:	SFEsdl-pango-devel
BuildRequires:	SUNWgnome-common-devel

%prep
%setup -q -n frozen-bubble-%{version}
%patch1 -p1

%build
make LIBDIR=%{_basedir}/perl5 BINDIR=%{_basedir}/bin DATADIR=%{_basedir}/share

%install
rm -f server/.depend
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_basedir}/bin \
             DATADIR=%{_basedir}/share LIBDIR=%{_basedir}/perl5 \
             INSTALLSITELIB=%{_basedir}/perl5/vendor_perl/%{perl_version} \
             INSTALLSITEARCH=%{_basedir}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
             PREFIX=%{_basedir}

rm -rf $RPM_BUILD_ROOT%{_basedir}/lib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_basedir}/perl5
%{_basedir}/perl5/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, sys) %{_datadir}/frozen-bubble
%{_datadir}/frozen-bubble/*

%changelog
* Sat Nov 19 2011 - Milan Jurik
- add IPS package name, cleanup
* Sun Apr 11 2010 - Milan Jurik
- adding missing build deps
* Mon Jan 12 2009 - alfred.peng@sun.com
- Initial version
