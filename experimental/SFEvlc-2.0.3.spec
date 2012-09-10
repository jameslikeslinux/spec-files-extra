#
# spec file for package SFEvlc
#
# includes module(s): vlc
#

%define debug_build 1

##TODO## re-enable and test taglib later
%define enable_taglib 0
%define enable_matroska 1
%define enable_libumem 1

##NOTE## If you run into compile problems and "vlc-cache-gen" core dumps,
#        then you *first* uninstall the old copy of vlc and re-try. 

##NOTE## if you are adding C++ compiled libraries, you need them compiled
#        with g++ ! .. you can use location /usr/g++/lib and /usr/g++/include 
#        to keep those external libraries separated from the SolStudio C++ 
#        compiled libs

##TODO##
#see this notes below, we might want those features compiled in,
#then we need to put BuildRequires and maybe need to make new 
#additional spec files 


##TODO##
#'t find: SFElibdts developer/documentation-tool/gtk SUNWsmbau SUNWgtk
#00:58 < Hazelesque2> and it complains that SUNWxwplt matches multiple packages
#solution: resolveipspacakges removes the "-doc" from developer/documentation-tool/gtk-doc in error
#pfexec pkg install developer/documentation-tool/gtk-doc
#then re-run the resolveipspackages script


# NOTE EXPERIMENTAL - current stat: 1.1.4.1 compiles, really needs a smart solution for NAME_MAX
#                     see patch header in Patch24 vlc-24-1114-NAME_MAX-dirty-fix-need-rework-x11_factory.cpp.diff,
#                     needs review of disabled patches if they still apply to 1.1.4.1,
#                     X consolidation for build 153 adds "x11-xcb" which is needed for vlc to
#                     display video inside the main window (and more) - see http://twitter.com/#!/alanc/status/29060334076
#                     and http://bugs.opensolaris.org/bugdatabase/view_bug.do?bug_id=6667057 Fixed in: snv_153
#                     on old osbuilds you get two separate windows. on new osbuild xcb helps with videodisplay inside the vlc
#                     window


# NOTE EXPERIMENTAL - does contain a few null pointer uses, so you might want to  " LD_PRELOAD=/usr/lib/0@0.so.1 vlc  "
# NOTE EXPERIMENTAL - uses SFEqt-gpp which is installed in the new location /usr/g++ (GNU C++ library) - needs patching
# NOTE EXPERIMENTAL - patches from old revision are not all reviewd if they are still needed

# tickets
#
# Ticket #3034 (closed defect: fixed) https://trac.videolan.org/vlc/ticket/3034
#    confusing delayed Interface initialization failed message
#    Fixed by 1861697 


#  Ticket #3036 (reopened patch) https://trac.videolan.org/vlc/ticket/3036
#    vlc-config calls /bin/sh but uses bash-isms

#  Ticket #3033 (new defect) https://trac.videolan.org/vlc/ticket/3033
#    lazy use of NULL pointers causes segfaults on Solaris

#  Ticket #3039 (new defect) https://trac.videolan.org/vlc/ticket/3039
#    no MMX symbols on Solaris 10?


# ticket worked around here in he spec-file (see tickets related to patches below in the patch section)
#  Ticket #3035 (closed defect: fixed) https://trac.videolan.org/vlc/ticket/3035
#    Solaris needs explicit -lsocket
#    Fixed by d17b37c 


%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%if %arch_sse2
#######%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2
%include x86_sse2.inc
%endif
 
%include base.inc

##TODO## use pnm_macros to determine which osdistro/osbuild needs SFE or SUNW libsdl
%define SFEsdl      %(/usr/bin/pkginfo -q SFEsdl && echo 1 || echo 0)

#new with 2.x.x source comes compressed in xz
BuildRequires:	%{pnm_buildrequires_SFExz}

#we have new X-org with x11-xcb CR 6667057
##TODO## check if other solarish OS do have same x11-xcb integrated with build 153
%if %( expr %{osbuild} '>=' 153 )
%define enable_x11_xcb 1
# more fresh builds all use IPS long package names
BuildRequires: x11/library/libxcb
Requires: x11/library/libxcb
%else
%define enable_x11_xcb 0
%endif

#just in case it is present, use SFElibxcb-devel anyways
##%if %(/usr/bin/pkginfo -q SFElibxcb && echo 1 || echo 0)
##%define enable_x11_xcb 1
##BuildRequires: SFElibxcb-devel
##Requires: SFElibxcb
##%endif

##TODO## temporarily disable building samba support (needs better detection
#  where smbclient.so lives)
%define enable_samba 0

##TODO## temporarily disable building pulseaudio support
%define enable_pulseaudio 0


%define	src_name	vlc
%define	src_url		http://download.videolan.org/pub/videolan/vlc

Name:                   SFEvlc
Summary:                vlc - multimedia player and streaming server
Version:                2.0.3
Source:                 %{src_url}/%{version}/%{src_name}-%{version}.tar.xz
Patch3:                 vlc-03-1141-oss.diff

## reminder: review if patches 4 .. 18 still valid/needed,
## just because something compiles doesn't mean a temporarily 
## disabled patch is not longer needed
## remove this note once the spec file leaves experimental/*
#Patch21:               vlc-21-1114-filesystem.c-NAME_MAX.diff
#Patch22:               vlc-22-remove-dirent.h-checks.diff
#Patch23:               vlc-23-1114-dirfd.diff
#Patch24:               vlc-24-1114-NAME_MAX-dirty-fix-need-rework-x11_factory.cpp.diff
##TODO## vlc-25-1111 needs a better solution
#Patch25:               vlc-25-1111-hack-define-posix_fadvise.diff
Patch28:               vlc-28-203-missing-system-include.diff

#note: ts.c:2455:21: error: implicit declaration of function 'dvbpsi_SDTServiceAddDescriptor'
#needs libdvbpsi >=0.1.6


IPS_package_name: media/vlc

#Meta(info.maintainer):          
Meta(info.upstream):            vlc@videolan.org
Meta(info.upstream_url):        http://www.videolan.org
#Group:	Applications/Sound and Video
Meta(info.classification):        org.opensolaris.category.2008:Applications/Sound and Video



SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

##TODO## check for a pnm_macro to fetch SFEsdl (depends on the addon SFEsdl-image below)
%if %SFEsdl
BuildRequires:  SFEsdl-devel
Requires:       SFEsdl
BuildRequires:  SFEsdl-image-devel
Requires:       SFEsdl-image
%else
BuildRequires:  SUNWlibsdl-devel
Requires:       SUNWlibsdl
##TODO## check if sdl-image is integrated or still needed separatly
%endif
Requires:       SUNWhal
BuildRequires:  SUNWdbus-devel
Requires:       SUNWdbus
Requires:       SUNWxorg-clientlibs
%if %{enable_samba}
BuildRequires:  %{pnm_buildrequires_SUNWsmba}
Requires:  %{pnm_requires_SUNWsmba}
%endif
BuildRequires:  SFElibfribidi-devel
Requires:       SFElibfribidi
BuildRequires:  %{pnm_buildrequires_SUNWfreetype2}
Requires:       %{pnm_requires_SUNWfreetype2}
BuildRequires:  SFEliba52-devel
Requires:       SFEliba52
BuildRequires:  SFEffmpeg-devel
Requires:       SFEffmpeg
BuildRequires:  SFElibmad-devel
Requires:       SFElibmad
BuildRequires:  SFElibmpcdec-devel
Requires:       SFElibmpcdec
%if %{enable_matroska}
BuildRequires:  SFElibmatroska-gpp
Requires:       SFElibmatroska-gpp
%endif
BuildRequires:  SUNWogg-vorbis-devel
Requires:       SUNWogg-vorbis
BuildRequires:  SFElibdvbpsi-devel
Requires:       SFElibdvbpsi
BuildRequires:  SFElibdvdnav-devel
Requires:       SFElibdvdnav
BuildRequires:  SFElibdts-devel
Requires:  SFElibdts
BuildRequires:  SFElibcddb-devel
Requires:       SFElibcddb
BuildRequires:  SFElibmpeg2-devel
Requires:       SFElibmpeg2
BuildRequires:  SFElibupnp-devel
Requires:       SFElibupnp
BuildRequires:  SFEvcdimager-devel
Requires:       SFEvcdimager
BuildRequires:  SFElibx264-devel
Requires:       SFElibx264
BuildRequires:  SFElibtar-devel
Requires:       SFElibtar
BuildRequires:	SUNWlua
Requires:	SUNWlua
BuildRequires: SUNWlibgcrypt
BuildRequires: SUNWlibproxy
BuildRequires: SUNWgnome-vfs
BuildRequires: SUNWlibrsvg
BuildRequires: SFEtwolame
BuildRequires: SFEgcc
BuildRequires: SUNWavahi-bridge-dsd
BuildRequires: SUNWlibgpg-error
Requires: SUNWlibgcrypt
Requires: SUNWlibproxy
Requires: SUNWgnome-vfs
Requires: SUNWlibrsvg
Requires: SFEtwolame
Requires: SFEgccruntime
Requires: SUNWavahi-bridge-dsd
Requires: SUNWlibgpg-error
BuildRequires: SFEtwolame-devel
Requires: SFEtwolame
%if %{enable_taglib}
BuildRequires: SFEtaglib-devel
Requires: SFEtaglib 
%endif
BuildRequires: SFElibid3tag-devel
Requires: SFElibid3tag
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
BuildRequires: SFElame-devel
Requires: SFElame
BuildRequires: SFElibdvdcss-devel
Requires: SFElibdvdcss

%if %{enable_pulseaudio}
BuildRequires: %{pnm_buildrequires_pulseaudio}
Requires:      %{pnm_requires_pulseaudio}
%endif

BuildRequires: %{pnm_buildrequires_SUNWltdl}
Requires: %{pnm_requires_SUNWltdl}

##TODO## eventually can be omitted, or patched out of Makefile
##BuildRequires: SUNWgit

BuildRequires:	SFEqt-gpp-devel
Requires:	SFEqt-gpp

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
#don't unpack please
%setup -q -c -T -n vlc-%version
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)

#%patch3 -p1
#%patch21 -p1
#%patch22 -p1
#%patch23 -p1
#%patch24 -p1
#%patch25 -p1
%patch28 -p1

perl -w -pi.bak -e "s,#\!\s*/bin/sh,#\!/usr/bin/bash," `find . -type f -exec grep -q "#\!.*/bin/sh" {} \; -print | egrep -v "/libtool"`

##TODO## experimental
# text references
#perl -w -pi.bakztext -e "s, -z def,," libtool

#especially for configure.ac ....
perl -w -pi.bak2 -e "s,hostname -s,hostname," configure configure.ac 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
# ffmpeg is build with g++, therefore we need to build with g++

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"

##evil!!! export PATH=/usr/gnu/bin:$PATH
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ./m4"
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
#
#notes to flags:
# Ticket #3040 (closed defect: fixed) https://trac.videolan.org/vlc/ticket/3040
# need to define _XPG4_2 on Solaris

##TODO## why make an extra "-L/lib -R/lib" ... can't see why we should do this
#export CXXFLAGS="%cxx_optflags -fpermissive -D_XPG4_2 -D__EXTENSIONS__ -L/lib -R/lib"
export CXXFLAGS="%cxx_optflags -L/lib -R/lib -fpermissive -D_XPG4_2 -D__EXTENSIONS__"
export CFLAGS="%optflags -L/lib -R/lib -D_XPG4_2 -D__EXTENSIONS__ -L/usr/gcc/lib -R/usr/gcc/lib $GNULIB"

#give these flags only to the C-Pre-Processor
export CPPFLAGS="-I/usr/X11/include -I/usr/gnu/include -I/usr/include/libavcodec -I/usr/include/libavutil -I./include -D_XPG4_2 -D__EXTENSIONS__"

#extend CFLAGS and CPPFLAGS with more Include locations for special libraries
#live555 aka liveMedia
export EXTRA_CFLAGS="${EXTRA_CFLAGS} -I/usr/lib/live/liveMedia/include -I/usr/lib/live/groupsock/include -I/usr/lib/live/UsageEnvironment/include"

%if %{enable_matroska}
#to find matroska as g++ variant we use -I/usr/g++/include
export EXTRA_CFLAGS="${EXTRA_CFLAGS} -I/usr/g++/include"
%else
%endif

#OI doesnt know about O_DIRECTORY in open(2)
#we could patch out that from the source or add it speculatively here
#as external define
export EXTRA_CFLAGS="${EXTRA_CFLAGS} -DO_DIRECTORY=0x1000000"

export CFLAGS="${CFLAGS} ${EXTRA_CFLAGS}"
export CPPFLAGS="${CPPFLAGS} ${EXTRA_CFLAGS}"



%if %{debug_build}
##TODO## might need to filter out "-O<n>" flags to switch off optimization and help switch on debuging
export CFLAGS="$CFLAGS -g"
%else
export CFLAGS="$CFLAGS -O4"
%endif

export LD=/opt/dtbld/bin/ld-wrapper
export AR=/usr/bin/ar
export PATH=/usr/bin:$PATH
#-L/lib -R/lib might trigger finding wrong libgcc_s.so and libstdc++.so.6 export LDFLAGS="%_ldflags -L/lib -R/lib"
export LDFLAGS="%_ldflags"

#extend EXTRA_LDFLAGS with more library locations for special libraries
%if %{enable_matroska}
export EXTRA_LDFLAGS="${EXTRA_LDFLAGS} $X11LIB $GNULIB -lsocket -lxnet"
export EXTRA_LDFLAGS="${EXTRA_LDFLAGS} -L/usr/lib/live/liveMedia -L/usr/lib/live/groupsock -L/usr/lib/live/UsageEnvironment"
export EXTRA_LDFLAGS="${EXTRA_LDFLAGS} -R/usr/lib/live/liveMedia -R/usr/lib/live/groupsock -R/usr/lib/live/UsageEnvironment"
#to find matroska it is sufficient to add -L and -R/usr/g++/lib
export EXTRA_LDFLAGS="${EXTRA_LDFLAGS} -L/usr/g++/lib"
export EXTRA_LDFLAGS="${EXTRA_LDFLAGS} -R/usr/g++/lib"
%else
%endif

#vlc's  xcb_glx module core dumps if running with at lest Nvidia driver .280.
#contained in S11 FCS release (osbuild 175)
#workaround, to be checked if that is a performance penalty if using libumem 
#(just a guess, needs not be true!!)

%if %{enable_libumem}
export EXTRA_LDFLAGS="${EXTRA_LDFLAGS} -lumem"
%else
%endif

export LDFLAGS="${LDFLAGS} ${EXTRA_LDFLAGS}"

export CONFIG_SHELL=/usr/bin/bash

[ -L include/ffmpeg ] || ln -s /usr/include/libavcodec include/ffmpeg
perl -w -pi.bak3 -e "s,#\!\s*/bin/sh,#\!/usr/bin/bash," configure*

#let Qt modules in vlc have a good runtime search patch for libraries
[ -d pkgconfig ] || mkdir pkgconfig
#-L/usr/g++/lib -->> -L/usr/g++/lib -R/usr/g++/lib
sed -e '/^Libs:/s/-L\([^ ]*\)/-L\1 -R\1/' < /usr/g++/lib/pkgconfig/QtGui.pc > pkgconfig/QtGui.pc
sed -e '/^Libs:/s/-L\([^ ]*\)/-L\1 -R\1/' < /usr/g++/lib/pkgconfig/QtCore.pc > pkgconfig/QtCore.pc
export PKG_CONFIG_PATH=`pwd`/pkgconfig:/usr/g++/lib/pkgconfig:/usr/lib/pkgconfig

# invalid options: --enable-ffmpeg                     \
#./configure --help | gegrep -i3 ffm prints only --enable-merge-ffmpeg   merge FFmpeg-based plugins (default disabled)

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
	    --enable-shared			\
	    --disable-static			\
	    --enable-live555			\
	    --enable-real			\
	    --enable-realrtsp			\
            --disable-dvb                       \
            --enable-id3tag                     \
            --enable-merge-ffmpeg               \
            --enable-tremor                     \
            --enable-asademux                   \
            --enable-snapshot                   \
            --enable-aa                         \
            --enable-oss                        \
            --enable-shine                      \
            --enable-omxil                      \
            --enable-switcher                   \
            --enable-faad                       \
%if %{enable_x11_xcb}
            --enable-xcb                        \
%else
            --disable-xcb                       \
%endif
%if %{enable_samba}
            --enable-smb                        \
%else
            --disable-smb                        \
%endif
%if %{enable_pulseaudio}
            --enable-pulse                        \
%else
            --disable-pulse                        \
%endif
%if %{enable_taglib}
            --enable-taglib                    \
%else
            --disable-taglib                   \
%endif
%if %{enable_matroska}
            --enable-mkv                    \
%else
            --disable-mkv                   \
%endif
%if %debug_build
	    --enable-debug=yes			\
%endif
            --disable-libva                   \
	    $nlsopt

#           --with-gnu-ld                       \
#test with this off	    --disable-rpath			\


%if %build_l10n
printf '%%%s/\/intl\/libintl.a/-lintl/\nwq\n' | ex - vlc-config
%endif


##TODO## investigate. Test if this goes away with new vlc version
#sometimes it fails with a core dump at vlc-cache-gen, just try again.
#does vlc-cache-gen work at all?
gmake -j$CPUS || echo "gmake 1. run failed, start over without vlc-cache-gen..."
mv bin/vlc-cache-gen bin/vlc-cache-gen.orig
touch bin/vlc-cache-gen
chmod a+rx bin/vlc-cache-gen
gmake
##NOTE## If you run into compile problems and "vlc-cache-gen" core dumps,
#        then you *first* uninstall the old copy of vlc and re-try. 

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
#Fix for disabled because core dumping vlc-cache-gen
cp -p bin/vlc-cache-gen.orig $RPM_BUILD_ROOT/%{_libdir}/vlc/vlc-cache-gen
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
find $RPM_BUILD_ROOT%{_libdir}/ -name '*.la' -exec rm {} \;
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then 
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor  || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vlc
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/vlc*
%{_libdir}/libvlc*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256/apps
%{_datadir}/icons/hicolor/16x16/apps/*
%{_datadir}/icons/hicolor/32x32/apps/*
%{_datadir}/icons/hicolor/48x48/apps/*
%{_datadir}/icons/hicolor/128x128/apps/*
%{_datadir}/icons/hicolor/256x256/apps/*
%dir %attr (-, root, other) %{_datadir}/kde4
%dir %attr (-, root, other) %{_datadir}/kde4/apps
%dir %attr (-, root, other) %{_datadir}/kde4/apps/solid
%dir %attr (-, root, other) %{_datadir}/kde4/apps/solid/actions
%{_datadir}/kde4/apps/solid/actions/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
#%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/lib*.a
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Aug  6 2012 - Thomas Wagner
- make vlc work with xz compressed source tarball, tested with pkgbuild 1.3.103 + 1.3.104
* Sat Aug  4 2012 - Thomas Wagner
- bump to 2.0.3 (build works with ffmpeg 0.11.1)
- add patch28 vlc-28-203-missing-system-include.diff, add -DO_DIRECTORY=0x1000000 missing only on OI open(2)
* Sat Aug  4 2012 - Thomas Wagner
- bump to 1.1.13 (build broke with ffmpeg)
- remove obsolete patch26 pulseaudio
#Patch27:               vlc-27-1112-xcb-xvideo.c-fix-memory-leak_remove-for-vlc-1.2.diff
- temporarily disable libva - not available (hardware accelleration)
* Sat Apr 28 2012 - Thomas Wagner
- remove -L/lib -R/lib from LDFLAGS (don't stuble over wrong gcc runtime libgcc_s.so libstdc++.so.6
- add missing (Build)Requires SFElibdvdcss
- now really find SFEmatroska-gpp (gcc compiled) in -L/usr/g++/lib -R/usr/g++/lib
* Sat Dec  3 2011 - Thomas Wagner
- add patch27 vlc-27-1112-xcb-xvideo.c-fix-memory-leak_remove-for-vlc-1.2.diff fixed
  in vlc-1.2.* http://www.mail-archive.com/vlc-commits@videolan.org/msg07284.html
- add temporarily check for present SFEsdl, to be changed into a pnm_macro 
  with a check on the osbuild introducting SUNWlibsdl
- switch for (Build)Requires x11/library/libxcb in case osbuild >= 153
- bump to 1.1.12 (again after repair/merge with 1.1.11)
- use again renamed patch vlc-26-1112-pulseaudio.diff
- add patch vlc-27-1112-xcb-xvideo.c-fix-memory-leak_remove-for-vlc-1.2.diff (thanks to EC)
- change (Build)Requires to g++ variant SFElibmatroska-gpp (instead of SFElibmatroska)
- make SFElibmatroska-gpp and SFEtaglib switchable, taglib *disabled* (enable again later)
  add includes only conditionally and use EXTRA_LDFLAGS / EXTRA_CFLAGS
- re-enable SFEtwolame/SFElame
- CFLAGS add -L/usr/gcc/lib -R/usr/gcc/lib
- use libumem (-l umem) to avoid core dumps at startup when loading modules and
  at program exit. To be monitored it the use of libumem changes performance.
  might avoid core dumps in some cases with xcb_glx nvidia module .280.
- add missing (Build)Requires: SFElibdvdcss(-devel)
* Tue Nov 29 2011 - Thomas Wagner
- re-work starting from 1.1.11 svn rev pre-3893 to maintain the SVN LOG !!
- repair patches format, merge spec changes for 1.1.12, re-add patches/vlc-26-1112-pulseaudio.diff
  (former wrong patch name: portaudio)
- repair liveMedia, matroska,  detection (rework *FLAGS for that)
- works on Solaris 11 11/11
- disable taglib as source for plugin loading errors, vlc-cache-gen core dump, 
  vlc program-end core dump. Is taglib evil?
* Wed Oct 19 2011 - Ken Mays <kmays2000@gmail.com>
- Major review and analysis
* Tue Oct 18 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 1.1.12
- Reviewed for Crash issues and future PulseAudio 1.0 support
- Resolves security issue in the HTTP and RTSP server components
* Fri Aug 26 2011 - Thomas Wagner
- add $GNULIB to CFLAGS, trying to avoid ldd /usr/bin/vlc print that 
  libgcc_s.so.1 not found (vlc works anyways, modules might pull that in)
- add note: if vlc is installed on the system, then vlc-cache-gen core dumps
  workaround: *uninstall* the existing vlc from the system, then re-run the spec
* Thu Aug 23 2011 - Thomas Wagner
- --disable-portaudio (might pkg-config add the switch -mt ? breaks vlc build)
- add LD=/opt/dtbld/bin/ld-wrapper to prevent gnu-ld jump in
- add AR=/usr/bin/ar to prevent gnu-ar jump in
- --disable twolame for a while, might not be necessary (re-check this).
  Check matching IPS package name, then re-enable if needed and uncomment (Build)Requires
- hardcode /usr/bin at the beginning of $PATH (or fails with archiver error)
- remove -D_XPG6 - gcc 4.5.x works again
* Mon Aug 15 2011 - Thomas Wagner
- bump to 1.1.11
##TODO## make ffmpeg optimized libs be found in pentiumpro+mmx libdir
##TODO## gcc 4.5.3 error 'asm' undeclared
- gcc 4.5.3 errors with misc/cpu.c:161:5: error: 'asm' undeclared - needs more love
- add patch25 vlc-25-1111-hack-define-posix_fadvise.diff - needs more love
- add (Build)Requires %{pnm_buildrequires_SUNWltdl} 
- replace osdistro.inc with packagenamemacros.inc
- make conditional (Build)Requires: %{pnm_buildrequires_SUNWsmba}
- change to (Build)Requires: %{pnm_buildrequires_SUNWfreetype2}
- quick add "needs more love" (Build)Requires:  SUNWlibgcrypt SUNWlibproxy 
  SUNWgnome-vfs SUNWlibrsvg SFEtwolame SFEgccruntime SUNWavahi-bridge-dsd SFElibgpg-error
- add on suspicion (Build)Requires: %{pnm_buildrequires_SUNWltdl}
- add for testing (might be omitted) BuildRequires: SUNWgit
- play with CFLAGS/CXXFLAGS/CPPFLAGS: remove -D__C99FEATURES__ , add -D_XPG6 ,
  CPPFLAGS remove -D__STDC_ISO_10646__ ,
  add  -fpermissive ... gcc 4.6.1 works, gcc 4.5.3 fails
- rewrite into temp-pc-files: QtGui.pc + QtCore.pc to include -R/usr/g++/lib, 
  then tweak PG_CONFIG_PATH to first find temp-pc-files, then /usr/g++, then system
- removed on suspicion  --disable-rpath  from configure
- removed wrong perl s/spatializer// on vlc-config
* Sat Aug  6 2011 - Thomas Wagner
- use Build(Requires) SFEqt-gpp(-devel) in /usr/g++, create local modified copy
  of QtGui.pc QtGui.pc to include -R/usr/g++/lib as well (or libQt* not found)
- ##TODO## temporarily disable building samba support (needs better detection 
  where smbclient.so lives)
- user QT4_LIBS and QT4_CFLAGS to override what pkg-config thinks (or at runtime
  qt not found or get with -L and added -R compile errors
- configure switches for xcb, samba (temp-disabled), pulseaudio (temp-disabled)
- configure switch --disable-mmx (video_*) does not compile
- ../bin/vlc-cache-gen (plugins) fails once, just re-run gmake in that case
- adjust %files
* Sat Mar 26 2011 - Thomas Wagner
- use SFEqt47-gpp with new Path layout, add PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig fo find QT
- add (Build)Requires:  SFElua
- create symlink for ffmpeg only if not already there
* Thu Nov 11 2010 - Thomas Wagner
- bump tp 1.1.4.1
- switch to gmake to have 3.81 version at least (old cbe 1.6.2 uses gmake 3.80)
- adjust %install for icons (remove extra mkdir/copy), add new icon directories to %files
- add patches ......  vlc-21-1114-filesystem.c-NAME_MAX.diff, vlc-22-remove-dirent.h-checks.diff
  vlc-23-1114-dirfd.diff, vlc-24-1114-NAME_MAX-dirty-fix-need-rework-x11_factory.cpp.diff
- rework/name_new patches vlc-03-1.1.4.1-oss.diff, ......
- remove patches ......
- build with mmx
- build with mpeg2
- enable or disable new xcb of xorg has x11-xcb integrated (%osbuild >= 153, CR 6667057)
- add (Build)Requires:  SUNWlibxcb(-devel) if %osbuild >= 153
- note: ts.c:2455:21: error: implicit declaration of function 'dvbpsi_SDTServiceAddDescriptor'
  needs libdvbpsi >=0.1.6 - upgrade your package with SFElibdvbpsi.spec (updated to 0.1.7)
* Aug 26 2009 - Gilles dauphin
- add patch , avoid empty struct for SS12
* Fri Aug 14 2009 - Thomas Wagner
- copy to encumbered/SFEvlc-1.0.1-experimental.spec
- remove patch11 libprostproc detection is upstream
- rework some patches for vlc-1.0.1
- still does not link correctly with sun and gnu linker - volunteers welcome, please get in contact
* April 2009 - Gilles Dauphin
- postprocess.h is in libpostproc
- TODO upgrade vlc, that's a nightmare
* Thu Dec 02 2008 - dauphin@enst.fr
- try to use the actual SFE ffmpeg , probleme in new ffmpeg API
- I just resign now, but... later i will retry
- TODO link to libpostproc: s/postproc/libpostproc/ .
* Thu Aug 07 2008 - trisk@acm.jhu.edu
- Rename SFElibdvdread dependency to SFElibdvdnav
* Fri Aug  3 2007 - dougs@truemail.co.th
- Added devel and l10n
- Added options to better find codecs
- Added icons for app
* Tue Jul 31 2007 - dougs@truemail.co.th
- added --disable-rpath option
- added SFElibx264 to the requirements
* Sun Jul 15 2007 - dougs@truemail.co.th
- --with-debug enables --enable-debug, added some dependencies
* Sat Jul 14 2007 - dougs@truemail.co.th
- Build with gcc
* Fri Mar 23 2007 - daymobrew@users.sourceforge.net
- Add two patches, 01-configure-no-pipe and 02-solaris. Add multiple
  dependencies. Getting closer but not quite building yet.
  Patch 01-configure-no-pipe removes the '-pipe' test. It causes problems later
  with -DSYS_SOLARIS being added after -pipe and being rejected by the linker.
  Patch 02-solaris.diff fixes two compiler issues. First involves expansion of
  ?: code; second changes AF_LOCAL to AF_UNIX as the former is not defined in
  <sys/socket.h>.

* Thu Mar 22 2007 - daymobrew@users.sourceforge.net
- Initial version

