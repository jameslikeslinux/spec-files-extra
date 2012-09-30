#
# spec file for package SFEmplayer2
#
# includes module(s): mplayer2
#

# mplayer2 is a fork of mplayer started in 2009.  A comparison of the two
# can be found here: http://www.mplayer2.org/comparison.html

# NOTE: To make man display the man page correctly, use
#	export PAGER="/usr/bin/less -insR"

# NOTE: mplayer2 does not come with MEncoder, because, according to the
#	mplayer2 Web site, "The MEncoder codebase was in very bad shape."

# NOTE: To allow mplayer and mplayer2 to be installed at the same time,
#	build with "pkgbuild --with-rename", which renames mplayer and
#	its man pages to "mplayer2".
%define rename %{?_with_rename:1}%{?!_with_rename:0}

%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include base.inc

%define snap 20111029

%define with_fribidi %(pkginfo -q SFElibfribidi && echo 1 || echo 0)
#%define with_ladspa %(pkginfo -q SFEladspa && echo 1 || echo 0)
%define with_openal %(pkginfo -q SFEopenal && echo 1 || echo 0)
#%define with_liba52 %(pkginfo -q SFEliba52 && echo 1 || echo 0)
#%define with_mpcdec %(pkginfo -q SFElibmpcdec && echo 1 || echo 0)
%define with_openjpeg %(pkginfo -q SFEopenjpeg && echo 1 || echo 0)
%define with_giflib %(pkginfo -q SFEgiflib && echo 1 || echo 0)
%define with_alsa %(pkginfo -q SFEalsa-lib && echo 1 || echo 0)
%define SFElibsndfile %(pkginfo -q SFElibsndfile && echo 1 || echo 0)
%define with_libdca %(pkginfo -q SFElibdts && echo 1 || echo 0)

Name:                    SFEmplayer2
IPS_Package_Name:	 media/mplayer2 
Summary:                 MPlayer fork with some additional features
License:                 GPLv3
SUNW_Copyright:	         mplayer2.copyright
Version:                 2.0.0.%snap
URL:                     http://www.mplayer2.org/
#Source:                 http://ftp.mplayer2.org/pub/release/mplayer2-%version.tar.xz
# Use the development version, since current release is incompatible
# with the new ffmpeg API
Source: http://git.mplayer2.org/mplayer2/snapshot/mplayer2-master.tar.bz2
Patch3:                  mplayer-snap-03-ldflags.diff
Patch4:                  mplayer2-04-realplayer.diff
Patch5:                  mplayer2-05-cpudetect.diff
#https://bugs.archlinux.org/task/28759
Patch7:			mplayer2-07-liveMedia.diff
Patch8:			mplayer2-08-liveMedia-config.diff
Patch9:			mplayer2-09-rpath.diff
Group:		Applications/Sound and Video
SUNW_BaseDir:            %_basedir
BuildRoot:               %_tmppath/%name-build

%include default-depend.inc
Requires: SUNWxorg-clientlibs
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWspeex
Requires: SUNWjpg
Requires: SUNWpng
Requires: SUNWogg-vorbis
Requires: SUNWlibtheora
BuildRequires: %{pnm_buildrequires_SUNWsmba}
Requires: %{pnm_requires_SUNWsmba}
BuildRequires: SFEffmpeg-devel
Requires: SFEffmpeg
Requires: SFEliveMedia
BuildRequires: SFEliveMedia
Requires: SFElibcdio
Requires: SFElibdvdnav
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
%ifarch i386 amd64
BuildRequires: SFEyasm
%endif
BuildRequires: SFElibcdio-devel
BuildRequires: SFElibdvdnav-devel
BuildRequires: SUNWgroff
BuildRequires: SUNWesu
Requires: driver/graphics/nvidia
BuildRequires: driver/graphics/nvidia

%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

Requires: SFElibmpcdec
BuildRequires: SFElibmpcdec-devel
%if %with_fribidi
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel
%endif
Requires: SFEladspa
BuildRequires: SFEladspa-devel
Requires: SFEmpg123
BuildRequires: SFEmpg123-devel
Requires: SFEliba52
BuildRequires: SFEliba52-devel
%if %with_openal
Requires: SFEopenal
BuildRequires: SFEopenal-devel
%endif
%if %with_openjpeg
Requires: SFEopenjpeg
BuildRequires: SFEopenjpeg-devel
%endif
%if %with_giflib
Requires: SFEgiflib
BuildRequires: SFEgiflib-devel
%endif
%if %with_alsa
BuildRequires: SFEalsa-lib
Requires: SFEalsa-lib
%endif
BuildRequires: SFElibass-devel
Requires: SFElibass
BuildRequires: SUNWttf-dejavu
Requires: SUNWttf-dejavu
%if %with_libdca
BuildRequires: SFElibdts-devel
Requires: SFElibdts
%endif
BuildRequires: SFEpython3

%define x11	/usr/openwin
%ifarch i386 amd64
%define x11	/usr/X11
%endif

%prep
#%setup -q -n mplayer2-%version
%setup -q -n mplayer2-master
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%if %debug_build
dbgflag=--enable-debug
export CFLAGS="-g -D__hidden=\"\""
%else
dbgflag=--disable-debug
export CFLAGS="-O2 -march=prescott -fomit-frame-pointer -D__hidden=\"\""
%endif

export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib -liconv" 
export CC=gcc

# On some Intel CPUs, ffmpeg incorrectly builds libraries for AMD
%define noamd3d %(prtdiag -v | grep CPU | grep -q Intel && echo 1 || echo 0)
%if %noamd3d
echo "hwcap_1 = V0x00800 V0x01000 OVERRIDE;" > mapfile
%else
echo "hwcap_1 = SSE;" > mapfile
%endif

# Enabling gl makes mplayer crash before printing anything 
# when built with gcc 4.6.2 (OK on gcc 4.6.1).  Even with
# 4.6.1, using -vo gl produces crashes when it tries to play.
bash ./configure				\
	    --prefix=%_prefix			\
	    --mandir=%_mandir			\
            --libdir=%_libdir			\
            --confdir=%_sysconfdir		\
            --extra-cflags="-I/usr/lib/live" \
            --extra-ldflags="-L/usr/lib/live/liveMedia -R/usr/lib/live/liveMedia -L/usr/lib/live/groupsock -R/usr/lib/live/groupsock -L/usr/lib/live/UsageEnvironment -R/usr/lib/live/UsageEnvironment -L/usr/lib/live/BasicUsageEnvironment -R/usr/lib/live/BasicUsageEnvironment -Wl,-Mmapfile" \
            --extra-libs="-lBasicUsageEnvironment -lUsageEnvironment -lgroupsock -lliveMedia -lstdc++ -liconv" \
            --enable-faad			\
            --disable-mad			\
            --disable-gl			\
            --enable-3dnow			\
            --enable-3dnowext			\
            --enable-live			\
            --enable-rpath			\
            --enable-runtime-cpudetection	\
	    --enable-crash-debug		\
	    $dbgflag

gmake -j$CPUS 


%install
rm -rf %buildroot
gmake install DESTDIR=%buildroot
%if %rename
mkdir %buildroot/%_datadir/mplayer2
ln -s /usr/openwin/lib/X11/fonts/TrueType/FreeSerif.ttf \
      %buildroot/%_datadir/mplayer2/subfont.ttf
%else
mkdir %buildroot/%_datadir/mplayer
# The following font is not supplied by OpenIndiana
#ln -s /usr/openwin/lib/X11/fonts/TrueType/FreeSerif.ttf \
ln -s /usr/share/fonts/TrueType/dejavu/DejaVuSans.ttf \
      %buildroot%_datadir/mplayer/subfont.ttf
%endif

%if %rename
cd %buildroot/%_bindir
mv mplayer mplayer2
cd ../share/man/man1
mv mplayer.1 mplayer2.1
%endif

# nroff does not understand macros used by mplayer man page
# See http://www.mplayerhq.hu/DOCS/tech/manpage.txt
#mkdir %buildroot/%_datadir/man/cat1
cd %buildroot/%_datadir/man
#cd ..
mkdir cat1
%if %rename
groff -mman -Tutf8 -rLL=78n man1/mplayer2.1 | col -bxp > cat1/mplayer2.1
%else
groff -mman -Tutf8 -rLL=78n man1/mplayer.1 | col -bxp > cat1/mplayer.1
%endif

rm -rf %buildroot/%_libdir
rm -rf %buildroot/%_sysconfdir
mkdir %buildroot%_docdir

%clean
rm -rf %buildroot


%files
%define _pkg_docdir %_docdir/mplayer
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %dir %_docdir
%doc README AUTHORS LICENSE
%_bindir/*
%_mandir/man1
%_mandir/cat1
%if %rename
%_datadir/mplayer2/subfont.ttf
%else
%_datadir/mplayer/subfont.ttf
%endif

%changelog
* Sun Apr 29 2012 - Pavel Heimlich
- make mplayer2 work with current liveMedia
* Tue Jan 24 2012 - James Choi
- Intel/AMD detection override
* Mon Dec 12 2012 - Thomas Wagner
- change to (Build)Requires pnm_requires_SUNWsmba
* Thu Nov 17 2011 - Alex Viskovatoff
- Add optional dependency on SFElibdts; disable esd (not part of Solaris 11)
* Sun Oct 30 2011 - Alex Viskovatoff
- Update tarball and switch to new versioning scheme
- Disable gt (causes crashes with gcc 4.6.2) and enable runtime cpu detection
* Wed Oct 19 2011 - Alex Viskovatoff
- Enable 3dnow and 3dnowext; add missing (build) dependency on SFEmpg123
- Disable libmad (only used on integer-only platforms, unsupported by SFE)
- Remove --enable-dynamic-plugins (deprecated by upstream)
* Fri Aug  5 2011 - Alex Viskovatoff
- Require driver/graphics/nvidia
* Wed Aug  3 2011 - Alex Viskovatoff
- Add missing (build) dependency on SFElibdvdnav
* Fri Jul 22 2011 - Alex Viskovatoff
- Default to not renaming mplayer to "mplayer2"; symlink to a DejaVu font
  which is available on all platforms; add SUNW_Copyright
* Sat Jul 16 2011 - Alex Viskovatoff
- Update to git version, so mplayer2 can link against newest ffmpeg
* Mon May  2 2011 - Alex Viskovatoff
- Fork SFEmplayer2.spec off SFEmplayer-snap.spec, making the appropriate changes
- Rename everything "mplayer2" for now so can coexist with original mplayer
* Wed Apr 27 2011 - Alex Viskovatoff
- Add missing optional dependencies
* Sat Apr  2 2011 - Alex Viskovatoff
- Update to new tarball
* Tue Jan 18 2011 - Alex Viskovatoff
- Update to new tarball, with Patch6 no longer required
- Replace --without-gui option with --with-gui, disabling gui by default
* Fri Nov  5 2010 - Alex Viskovatoff
- Use fixed (constant) tarball from Arch Linux repository by default
- Remove obsolete configure switch --enable-network
- Restore cpu detection patch by Milan Jurik
- Add Patch6 by Thomas Wagner to make mkstemp get used
- Add --without-gui option: the configure default is to disable the gui,
  and the MPlayer download page effectively deprecates the included gui
- Create a formatted man page, since nroff cannot handle the man page
* Wed Aug 18 2010 - Thomas Wagner
- rename configure switch --enable-faad-external to --enable-faad   
- use gmake in %build instead make (might have solved makefile syntax error)
* Fri May 21 2010 - Milan Jurik
- openjpeg and giflib support
* Thu Aug 20 2009 - Milan Jurik
- -fomit-frame-pointer to workaround Solaris GCC bug on Nehalem
* Sun Aug 16 2009 - Milan Jurik
- GNU grep not needed
* Sat Jul 18 2009 - Milan Jurik
- improved handling of tarball
* Sat Jul 11 2009 - Milan Jurik
- Initial version
