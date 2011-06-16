#
# Blender 2.57b SPEC file for SFE
# By Ken Mays
#
%include Solaris.inc
#
# Note: Blender 2.57b prefers Python 2.6.6 or higher.
#      
%define python_version 2.6
%define src_version 2.57b
%define src_url http://download.blender.org/source
%define collada 1 
%define wplayer 1 

Name:           SFEblender
Summary:        Blender -  the free open source 3D content creation suite
Version:        2.57.2
URL:		http://www.blender.org
Source:		%{src_url}/blender-%{src_version}.tar.gz
Patch1:		blender-2.57b-01-sunos5-config.diff	
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
Requires: 	SUNWpostrun
Requires:	SFEcmake
BuildRequires: 	SFEgcc
Requires: 	SFEgccruntime
BuildRequires: 	SUNWTiff
BuildRequires: 	SUNWopensslr
BuildRequires: 	SUNWlibsdl-devel
BuildRequires: 	SUNWPython
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

# Don't even think about trying to build this with Solaris Studio
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

export CFLAGS="$RPM_OPT_FLAGS -pipe -fopenmp -fPIC -funsigned-char -fno-strict-aliasing -g -ggdb" 
export CXXFLAGS=$CFLAGS
export BF_TIFF_LIB="%{_libdir}/libtiff.so" 
export BF_TIFF_INC="%{_includedir}" 
export BF_GETTEXT_LIBPATH="%{_libdir}" 
#WITH_INTERNATIONAL 
mkdir -p Build 
pushd Build 
#      -DPYTHON_LIB=%%{_libdir}/libpython2.6.so \ 
cmake ../ \ 
      -G"Unix Makefiles" \ 
      -DWITH_FFTW3:BOOL=on \ 
      -DWITH_JACK:BOOL=on \ 
      -DWITH_CODEC_SNDFILE:BOOL=on \ 
      -DWITH_IMAGE_OPENJPEG:BOOL=off \ 
%if %{collada} == 1 
      -DWITH_OPENCOLLADA:BOOL=on \ 
      -DOPENCOLLADA=%{_prefix} \ 
      -DOPENCOLLADA_LIBPATH=%{_libdir} \ 
      -DOPENCOLLADA_INC=%{_includedir} \ 
%else
      -DWITH_OPENCOLLADA:BOOL=off \ 
%endif
      -DPYTHON_LIBPATH=%{_libdir} \ 
      -DPYTHON_LIBRARY=%{_libdir}/libpython%{python3_ver}%{py3_abi_kind}.so \ 
      -DPYTHON_INCLUDE_DIRS=%{python3_incdir} \ 
      -DWITH_PYTHON_INSTALL:BOOL=off \ 
      -DWITH_PYTHON:BOOL=on \ 
      -DWITH_IMAGE_OPENJPEG:BOOL=off \ 
      -DWITH_GAMEENGINE:BOOL=on \ 
%if %DISTRIBUTABLE == 1 
      -DWITH_CODEC_FFMPEG:BOOL=off \ 
%else
      -DWITH_CODEC_FFMPEG:BOOL=on \ 
%endif
      -DWITH_CXX_GUARDEDALLOC:BOOL=on \ 
      -DCMAKE_VERBOSE_MAKEFILE:BOOL=on \ 
%if %wplayer == 1 
      -DWITH_PLAYER:BOOL=on \ 
%else
      -DWITH_PLAYER:BOOL=off \ 
%endif
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}

make -j$CPUS


%install


rm -rf $RPM_BUILD_ROOT
#mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
#cd blender-%{src_version}
#gmake release

# x86_64, i386, etc.
#cd obj/blender-%{version}-solaris-2.11-*-py%{python_version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/blender


cd .blender
tar cf - . | (cd $RPM_BUILD_ROOT%{_datadir}/blender ; tar xfp -)
cd ..

install -d -m 0755 $RPM_BUILD_ROOT/%{_bindir}
install -m 0755 blender $RPM_BUILD_ROOT%{_bindir}/blender
#install -m 0755 blenderplayer $RPM_BUILD_ROOT%{_bindir}/blenderplayer

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
%{_datadir}/pixmaps/blender.xpm 
%{_datadir}/icons/hicolor/16x16/apps/blender.png 
%{_datadir}/icons/hicolor/22x22/apps/blender.png 
%{_datadir}/icons/hicolor/32x32/apps/blender.png 
%{_datadir}/icons/hicolor/scalable/apps/blender.svg 
%{_datadir}/pixmaps/blender.svg 
%{_datadir}/pixmaps/blender.png 
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
* Mon 15 Jun 2010 - Ken Mays <kmays2000@gmail.com>
- Initial spec
