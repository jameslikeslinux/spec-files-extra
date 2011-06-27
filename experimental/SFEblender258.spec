#
# Blender 2.58(x) SPEC file for SFE
# By Ken Mays
#
%include Solaris.inc
#
# Note: Blender 2.58 prefers Python 3.2.x or higher.
# Note: FFMPEG and Boomer API audio header   
# Note: You can use Scons (preferred) or CMAKE. 
# 
%define python_version 3.2
%define src_version 2.58
%define src_url http://download.blender.org/source
%define collada 1 
%define wplayer 1 

Name:           SFEblender258
Summary:        Blender -  the free open source 3D content creation suite
Version:        2.58.0
URL:		http://www.blender.org
Source:		%{src_url}/blender-%{src_version}.tgz
Patch1:		blender-2.58-sunos5-config.diff	
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
Requires: 	SUNWlibsdl
Requires: 	SUNWopenexr
Requires: 	SUNWilmbase
Requires: 	SUNWfreetype2
Requires: 	SUNWpng
#Requires:	SUNWmesa
Requires:	SUNWpcre
#Requires:	SFEscons
Requires: 	SUNWpostrun
Requires:	system/header/header-audio
Requires:	library/expat
Requires:	library/perl-5/xml-parser
BuildRequires: 	SFEgcc
Requires: 	SFEgccruntime
BuildRequires: 	SUNWTiff
BuildRequires: 	SUNWopensslr
BuildRequires: 	SUNWlibsdl-devel
# Build Python 3.2.x 
#BuildRequires: 	SUNWPython
BuildRequires:	driver/graphics/nvidia

%description
Blender is a 3D modelling and rendering package. It is the in-house 
software of a high quality animation studio, Blender has proven to 
be an extremely fast and versatile design instrument. The software 
has a personal touch, offering a unique approach to the world of 
Three Dimensions. Use Blender to create TV commercials, to make 
technical visualizations, business graphics, to do some morphing, 
or design user interfaces. You can easy build and manage complex 
environments. The renderer is versatile and extremely fast. All 
basic animation principles (curves & keys) are well implemented.It 
includes tools for modeling, sculpting, texturing (painting, 
node-based shader materials, or UV mapped), UV mapping, rigging and 
constraints, weight painting, particle systems, simulation (fluids, 
physics, and soft body dynamics and an external crowd simulator), 
rendering, node-based compositing, and non linear video editing, 
as well as an integrated game engine for real-time interactive 3D 
and game creation and playback with cross-platform compatibility. 
http://www.blender.org 

Authors: 
-------- 
    Stichting Blender Foundation 
    Frederiksstraat 12-2
    1054 LC Amsterdam 
    the Netherlands 
    foundation(at)blender(dot)org 

%package root
Summary:         %summary - platform dependent files, / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:		 %summary - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -c -n %{name}
cd blender-%{src_version}
%patch1 -p1

%build

CPUS=$(psrinfo | awk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export PKG_CONFIG_PATH="$PROTO_PKG"

cd blender-%{src_version}

# SFEgcc 4.5.2
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

export CFLAGS="$RPM_OPT_FLAGS -march=pentium4 -pipe -fopenmp -fPIC -funsigned-char -fno-strict-aliasing -g -ggdb" 
export CXXFLAGS=$CFLAGS
#
# Note:     -DPYTHON_LIB=%%{_libdir}/libpython3.2.so \ 
#
# Prefer built-in Scons setup and make mods for GCC 4.5.2
#

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export MSGFMT=/usr/gnu/bin/msgfmt

#
# Used built-in scons 1.2.0 here
# build_files/scons/config/sunos5-config.py
#
python scons/scons.py -j $CPUS prefix=%{_basedir}       \
        python_site_packages_dir=%{pythonlibdir}


%install


rm -rf $RPM_BUILD_ROOT

python scons/scons.py install prefix=%{_basedir} python_site_packages_dir=%{pythonlibdir} \
        mandir=%{_mandir} destdir=$RPM_BUILD_ROOT


# x86_64, i386, etc.
#cd obj/blender-%{version}-solaris-2.11-*-py%{python_version}
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/blender

#%if %build_l10n
#%else
#rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
#%endif

%post
/usr/bin/update-mime-database "%{_datadir}/mime" >/dev/null 
  
%postun
/usr/bin/update-mime-database "%{_datadir}/mime" >/dev/null 
 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/blender 
%{_bindir}/blender-thumbnailer.py 
%{_bindir}/blender-sample 
%{_bindir}/blenderplayer 
%{_mandir}/man1/blender.1 
%{_mandir}/man1/blender.1.py
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/blender
%{_datadir}/applications/blender.desktop 
%{_datadir}/applications/x-blend.desktop 
%{_datadir}/locale/*
%{_datadir}/pixmaps/blender.xpm 
%{_datadir}/icons/hicolor/16x16/apps/blender.png 
%{_datadir}/icons/hicolor/22x22/apps/blender.png 
%{_datadir}/icons/hicolor/24x24/apps/blender.png
%{_datadir}/icons/hicolor/32x32/apps/blender.png 
%{_datadir}/icons/hicolor/48x48/apps/blender.png
%{_datadir}/icons/hicolor/256x256/apps/blender.png
%{_datadir}/icons/hicolor/scalable/apps/blender.svg 
%{_datadir}/pixmaps/blender.svg 
%{_datadir}/pixmaps/blender.png 
%{_datadir}/doc-base/*
%{_datadir}/blender/*  


#%if %build_l10n
#%files l10n
#%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
#%endif

#%files devel 
#%defattr(-,root,bin) 
#%dir %{_includedir}/%{name}/ 
#%{_includedir}/%{name}/*.h 
#%{_includedir}/%{name}/*.DEF 
  
%changelog
* Mon Jun 27 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2.58
* Mon 15 Jun 2011 - Ken Mays <kmays2000@gmail.com>
- Revised spec for Blender > 2.49b and Python 3.2 req
* May 18 2010 - G.D.
- exec in bindir
* Wed May 12 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 2.49b
- Update Python version to 2.6
- Fix install on non-amd64
- Create wrapper at build time
* Jue  17 2009 - Simonjin
- Bump to 2.49, and update the patch blender-01-build.diff
* April 2009 - Gilles dauphin
- adjust version for IPS
* Sun 18 Jan 2009 - Henry Zhang
- Bump to 2.48a, and update the patch and blender-01.sh.
* Thu 27 Nov 2008 - Henry Zhang
- Add dependency SUNWilmbase
* Sun 09 Nov 2008 - Gilles Dauphin
- depend SUNWopenexr
* Sept 16 2008 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
- Initial specc
