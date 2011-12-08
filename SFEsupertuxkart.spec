#
# spec file for package SFEsupertuxkart.spec
#
%include Solaris.inc

%define src_name supertuxkart
%define src_version 0.7.3

%define SFEsdl      %(/usr/bin/pkginfo -q SFEsdl && echo 1 || echo 0)
%define SFEplib_gpp %(/usr/bin/pkginfo -q SFEplib-gpp && echo 1 || echo 0)



Name:           SFEsupertuxkart
Version:        0.7.3
Summary:        Kids 3D go-kart racing game featuring Tux
Group:          Amusements/Games
License:        GPLv2+ and GPLv3 and CC-BY-SA
URL:            http://supertuxkart.sourceforge.net/
Source0:        %{sf_download}/%{src_name}/%{src_name}-%{src_version}-src.tar.bz2
Source2:	%{sf_download}/%{src_name}/STK_0.7_Karts_AddonsPack.7z
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%if %SFEplib_gpp
BuildRequires:  SFEplib-gpp
%define cc_is_gcc 1
%define _gpp g++
%include base.inc
BuildRequires: SFEgcc
Requires: SFEgccruntime
%else
BuildRequires:  SFEplib-devel
%endif

BuildRequires:  SUNWlibsdl-devel
Requires:	SUNWlibsdl
BuildRequires:	SUNWlibmikmod-devel
Requires:	SUNWlibmikmod
BuildRequires:  SUNWogg-vorbis-devel
Requires:	SUNWogg-vorbis
BuildRequires:	SFEfreeglut-devel
Requires:	SFEfreeglut
BuildRequires:  SFEopenal-devel
Requires:	SFEopenal
BuildRequires:	SFEfreealut-devel
Requires:	SFEfreealut
BuildRequires:	SUNWgawk
BuildRequires:	SUNWgnu-findutils
Requires:	SFEbullet
BuildRequires:	SFEplib-devel
Requires:	SFEplib

%description
3D go-kart racing game for kids with several famous OpenSource mascots
participating. Race as Tux against 3 computer players in many different fun
race courses (Standard race track, Dessert, Mathclass, etc). Full information
on how to add your own race courses is included. During the race you can pick
up powerups such as: (homing) missiles, magnets and portable zippers.

%package data
Summary:	%{summary} - data files
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%description data
This package contains the data files for SuperTuxKart, as well as the add-on pack.

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
%endif

%prep
%setup -q -n %{src_name}-%{src_version}
# some cleanups
chmod -x AUTHORS COPYING ChangeLog README TODO
chmod -x `find -name "*.cpp" -o -name "*.hpp"`
rm -fr data/karts/*/.svn data/karts/.svn

unzip %{SOURCE2} -d data/ -x karts/mriceblock*

%build
%if %SFEplib_gpp
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CXXFLAGS="-I%{_includedir} -I%{_prefix}/X11/include"
export LDFLAGS="-L%{_libdir} -R%{_libdir} -lGLU -lnsl -lsocket"
%else
export CXXFLAGS="%cxx_optflags -I%{_includedir} -I%{_prefix}/X11/include"
export LDFLAGS="%_ldflags -L%{_libdir} -R%{_libdir} -lGLU -lnsl -lsocket"
%endif
export PKG_CONFIG_PATH="%{_libdir}/pkgconfig"

autoconf
export ac_cv_member_struct_msghdr_msg_flags=no
./configure --prefix=%{_prefix} --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# easier then patching all the Makefile's
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_prefix}/games/%{src_name} $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_datadir}/games/%{src_name}/data/po $RPM_BUILD_ROOT%{_datadir}/locale
rmdir $RPM_BUILD_ROOT%{_prefix}/games

%if %build_l10n
# usr/share/locale/fr_CA should be in fr
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/fr_CA
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_prefix}
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/%{src_name}.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.xpm
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%files data
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/games/%{src_name}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
Thu Dec 8 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 0.7.3
Tue Oct 11 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 0.7.2
- Removed legacy Sun Studio patch
Wed Jun 8 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 0.7.1.b
- New addon STK_0.7_Karts_AddonsPack.7z
- Reviewed irrlicht-1.7.2 dependency 

* May 2010 - G.d.
- and other try

* Sun May 09 2010 - Gilles Dauphin
- search Openal in AL/al.h

* Sun May 09 2010 Milan Jurik
- initial SFE import

* Thu Jan 14 2010 Jon Ciesla <limb@jcomserv.net> - 0.6.2-3
- Rebuild for new irrlicht.

* Thu Nov 19 2009 Jon Ciesla <limb@jcomserv.net> - 0.6.2-2
- Add in addon pack.
- Split data to noarch subpackage.

* Thu Sep 10 2009 Jon Ciesla <limb@jcomserv.net> - 0.6.2-1
- Bugfix release.

* Sun Aug 16 2009 Hans de Goede <hdegoede@redhat.com> - 0.6.1a-3
- Switch to openal-soft

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Jon Ciesla <limb@jcomserv.net> - 0.6.1a-1
- Patch release.
- Fixed symlink/dir replacement, BZ 506245.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Hans de Goede <hdegoede@redhat.com> 0.6.1-1
- New upstream release 0.6.1

* Sun Jan 25 2009 Hans de Goede <hdegoede@redhat.com> 0.6-1
- New upstream release 0.6

* Sun Sep  7 2008 Hans de Goede <hdegoede@redhat.com> 0.5-2
- Fix patch fuzz build failure

* Tue Jun  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5-1
- New upstream release 0.5

* Tue May 13 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-2
- Rebuild for new plib

* Mon Mar 10 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-1
- New upstream release 0.4
- Note this version includes a build in copy of the bullet physics library,
  this is a patched copy making use if a system version impossible

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3-4
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-3
- Fix compilation with gcc 4.3

* Mon Sep 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-2
- Use opengl-games-utils wrapper to show error dialog when DRI is missing

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-1
- New upstream release 0.3
- Drop most patches (all fixed upstream)
- Update License tag for new Licensing Guidelines compliance

* Fri Oct  6 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-3
- replace some more coprighted images and sounds
- fix a bunch of joystick related bugs

* Mon Sep 25 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-2
- rename images-legal.txt to supertuxkart-images-legal.txt
- add a changelog entry for the previous release (and this one)

* Mon Sep 25 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-1
- initial Fedora Extras package (replacing regular tuxkart)
