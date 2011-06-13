#
# spec file for package: SFEmurrine-engine
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use murrine_64 = murrine-engine.spec
%endif
%include base.inc
%use murrine = murrine-engine.spec

Name:		SFEmurrine-engine
Version:	%{murrine.version}
Summary:	Gtk2 Engine Featuring a Modern Glassy Look
License:	GPLv2
Url:		http://www.cimitan.com/murrine/
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright:	%{name}.copyright

%include default-depend.inc
BuildRequires:	SUNWgnome-common-devel
BuildRequires:	SUNWgnu-gettext
BuildRequires:	SUNWxwinc
BuildRequires:	SUNWxorg-headers
Requires:	SUNWfontconfig
Requires:	SUNWfreetype2
Requires:	SUNWgnome-base-libs
Requires:	SUNWlexpt
Requires:	SUNWmlib
Requires:	SUNWpng
Requires:	SUNWxorg-clientlibs
Requires:	SUNWxwplt
Requires:	SUNWzlib

Meta(info.maintainer):		James Lee <jlee@thestaticvoid.com>
Meta(info.upstream):		Andrea Cimitan <andrea.cimitan@gmail.com>
Meta(info.upstream_url):	http://www.cimitan.com/murrine/
Meta(info.classification):	org.opensolaris.category.2008:Desktop (GNOME)/Theming

%description
Murrine is a Gtk2 engine, written in C language, using cairo vectorial drawing
library to draw widgets. It features a modern glassy look, and it is elegant
and clean on the eyes. It is also extremely customizable.

%package themes
Summary:	Themes for the Murrine engine by Cimi
Requires:	%{name}

%description themes
This package includes themes by Cimi for the Murrine Gtk2 engine.  The themes
include: MurrinaGilouche, MurrinaAquaish, MurrinaVerdeOlivo, MurrinaBlue,
MurrinaFancyCandy, MurrinaLoveGray, and MurrineRounded.

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
%ifarch amd64 sparcv9
mkdir %{name}-%{version}/%{_arch64}
%murrine_64.prep -d %{name}-%{version}/%{_arch64}
%endif
mkdir %{name}-%{version}/%{base_arch}
%murrine.prep -d %{name}-%{version}/%{base_arch}

%build
%ifarch amd64 sparcv9
%murrine_64.build -d %{name}-%{version}/%{_arch64}
%endif
%murrine.build -d %{name}-%{version}/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%murrine_64.install -d %{name}-%{version}/%{_arch64}
%endif
%murrine.install -d %{name}-%{version}/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/gtk-2.0/2.10.0/engines/libmurrine.so
%endif
%{_libdir}/gtk-2.0/2.10.0/engines/libmurrine.so
%attr(755,root,sys) %dir %{_datadir}
%{_datadir}/gtk-engines/murrine.xml

%files themes
%defattr(-,root,bin)
%attr(755,root,sys) %dir %{_datadir}
%{_datadir}/themes/MurrinaAquaIsh/gtk-2.0/gtkrc
%{_datadir}/themes/MurrinaFancyCandy/gtk-2.0/gtkrc
%{_datadir}/themes/MurrinaGilouche/gtk-2.0/gtkrc
%{_datadir}/themes/MurrinaLoveGray/gtk-2.0/gtkrc
%{_datadir}/themes/MurrinaVerdeOlivo/gtk-2.0/gtkrc
%{_datadir}/themes/MurrineRounded/metacity-1/menu-mur.png
%{_datadir}/themes/MurrineRounded/metacity-1/menu.png
%{_datadir}/themes/MurrineRounded/metacity-1/metacity-theme-1.xml
%{_datadir}/themes/MurrineRoundedIcon/metacity-1/metacity-theme-1.xml
%{_datadir}/themes/MurrineRoundedLessFramed/metacity-1/menu-mur.png
%{_datadir}/themes/MurrineRoundedLessFramed/metacity-1/menu.png
%{_datadir}/themes/MurrineRoundedLessFramed/metacity-1/metacity-theme-1.xml
%{_datadir}/themes/MurrineRoundedLessFramedIcon/metacity-1/menu-mur.png
%{_datadir}/themes/MurrineRoundedLessFramedIcon/metacity-1/menu.png
%{_datadir}/themes/MurrineRoundedLessFramedIcon/metacity-1/metacity-theme-1.xml


%changelog
* Mon Jun 13 2011 - jlee@thestaticvoid.com
- Update for SFE inclusion. 
* Sun May 31 2009 - jlee@thestaticvoid.com
- Add header and correct copyright
* Fri May 29 2009 - jlee@thestaticvoid.com
- Initial version
