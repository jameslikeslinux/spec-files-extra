#
# spec file for package SFEmplayer2
#
# includes module(s): mplayer2
#

# mplayer2 is a fork of mplayer started in 2009.
# We take the unconventional step of renaming the executable and
# man pages to "mplayer2", to allow both the original and the fork
# to be installed at the same time.

# NOTE: To make man display the man page correctly, use
#	export PAGER="/usr/bin/less -insR"

# NOTE: mplayer2 does not come with MEncoder, because, according to the
#	mplayer2 Web site, "The MEncoder codebase was in very bad shape."

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

# TODO: Since we now use SFEffmpeg, which pulls in a lot of media libs,
#	the conditional "requires" machinery below and further on is
#	probably superfluous.

%define with_faad %(pkginfo -q SFEfaad2 && echo 1 || echo 0)
%define with_fribidi %(pkginfo -q SFElibfribidi && echo 1 || echo 0)
%define with_ladspa %(pkginfo -q SFEladspa && echo 1 || echo 0)
%define with_openal %(pkginfo -q SFEopenal && echo 1 || echo 0)
%define with_mad %(pkginfo -q SFElibmad && echo 1 || echo 0)
%define with_liba52 %(pkginfo -q SFEliba52 && echo 1 || echo 0)
%define with_lame %(pkginfo -q SFElame && echo 1 || echo 0)
%define with_twolame %(pkginfo -q SFEtwolame && echo 1 || echo 0)
%define with_mpcdec %(pkginfo -q SFElibmpcdec && echo 1 || echo 0)
%define with_xvid %(pkginfo -q SFExvid && echo 1 || echo 0)
%define with_x264 %(pkginfo -q SFElibx264 && echo 1 || echo 0)
%define with_openjpeg %(pkginfo -q SFEopenjpeg && echo 1 || echo 0)
%define with_giflib %(pkginfo -q SFEgiflib && echo 1 || echo 0)
%define with_schroedinger %(pkginfo -q SFElibschroedinger && echo 1 || echo 0)
%define with_alsa %(pkginfo -q SFEalsa-lib && echo 1 || echo 0)

%define SFElibsndfile %(pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:                    SFEmplayer2
Summary:                 MPlayer fork with some additional features
Version:                 2.0
URL:                     http://www.mplayer2.org/
#Source:                  http://ftp.mplayer2.org/pub/release/mplayer2-%version.tar.xz
#Source:    http://git.mplayer2.org/mplayer2/snapshot/mplayer2-2.0.tar.bz2
Source: http://git.mplayer2.org/mplayer2/snapshot/mplayer2-master.tar.bz2
Patch1:                  mplayer-snap-01-shell.diff
Patch3:                  mplayer-snap-03-ldflags.diff
Patch4:                  mplayer-snap-04-realplayer.diff
Patch5:                  mplayer-snap-05-cpudetect.diff
SUNW_BaseDir:            %_basedir
BuildRoot:               %_tmppath/%name-build

%include default-depend.inc
Requires: SUNWsmbau
Requires: SUNWxorg-clientlibs
Requires: SUNWfontconfig
# OI 151 is at a newer version than S11X, so this dependency blocks installation on S11X
#Requires: SUNWfreetype2
Requires: SUNWspeex
Requires: SUNWjpg
Requires: SUNWpng
Requires: SUNWogg-vorbis
Requires: SUNWlibtheora
Requires: SUNWsmbau
BuildRequires: SFEffmpeg-devel
Requires: SFEffmpeg
Requires: SFEliveMedia
Requires: SFElibcdio
%ifarch i386 amd64
BuildRequires: SFEyasm
%endif
BuildRequires: SFElibcdio-devel
BuildRequires: SUNWgroff
BuildRequires: SUNWesu

%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

Requires: SFElame
BuildRequires: SFElame-devel
%if %with_twolame
Requires: SFEtwolame
BuildRequires: SFEtwolame-devel
%endif
Requires: SFEfaad2
BuildRequires: SFEfaad2-devel
Requires: SFElibmpcdec
BuildRequires: SFElibmpcdec-devel
%if %with_fribidi
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel
%endif
Requires: SFEladspa
BuildRequires: SFEladspa-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
Requires: SFEliba52
BuildRequires: SFEliba52-devel
%if %with_openal
Requires: SFEopenal
BuildRequires: SFEopenal-devel
%endif
%if %with_xvid
Requires: SFExvid
BuildRequires: SFExvid-devel
%endif
%if %with_x264
Requires: SFElibx264
BuildRequires: SFElibx264-devel
%endif
%if %with_openjpeg
Requires: SFEopenjpeg
BuildRequires: SFEopenjpeg-devel
%endif
%if %with_giflib
Requires: SFEgiflib
BuildRequires: SFEgiflib-devel
%endif
%if %with_schroedinger
BuildRequires: SFElibschroedinger
Requires: SFElibschroedinger
%endif
%if %with_alsa
BuildRequires: SFEalsa-lib
Requires: SFEalsa-lib
%endif
BuildRequires: SFElibass-devel
Requires: SFElibass

%define x11	/usr/openwin
%ifarch i386 amd64
%define x11	/usr/X11
%endif

%prep
#%setup -q -n mplayer2-%version
%setup -q -n mplayer2-master
%patch1 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%if %debug_build
dbgflag=--enable-debug
export CFLAGS="-g -D__hidden=\"\""
%else
dbgflag=--disable-debug
export CFLAGS="-O2 -fomit-frame-pointer -D__hidden=\"\""
%endif

# SFEgcc adds /usr/gnu/lib to lib search path
#export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib -liconv" 
export LDFLAGS="-liconv" 
export CC=gcc

bash ./configure				\
	    --prefix=%_prefix			\
	    --mandir=%_mandir			\
            --libdir=%_libdir			\
            --confdir=%_sysconfdir		\
            --enable-menu			\
            --extra-cflags="-I/usr/lib/live/liveMedia/include -I/usr/lib/live/groupsock/include -I/usr/lib/live/UsageEnvironment/include -I/usr/lib/live/BasicUsageEnvironment/include" \
            --extra-ldflags="-L/usr/lib/live/liveMedia -R/usr/lib/live/liveMedia -L/usr/lib/live/groupsock -R/usr/lib/live/groupsock -L/usr/lib/live/UsageEnvironment -R/usr/lib/live/UsageEnvironment -L/usr/lib/live/BasicUsageEnvironment -R/usr/lib/live/BasicUsageEnvironment" \
            --extra-libs="-lBasicUsageEnvironment -lUsageEnvironment -lgroupsock -lliveMedia -lstdc++ -liconv" \
%if %with_faad
            --enable-faad		\
%endif
            --enable-live			\
	    --enable-rpath			\
	    --enable-crash-debug		\
            --enable-dynamic-plugins            \
	    $dbgflag

gmake -j$CPUS 


%install
rm -rf %buildroot
gmake install DESTDIR=%buildroot
mkdir %buildroot/%_datadir/mplayer2
ln -s /usr/openwin/lib/X11/fonts/TrueType/FreeSerif.ttf \
      %buildroot/%_datadir/mplayer2/subfont.ttf

cd %buildroot/%_bindir
mv mplayer mplayer2
cd ../share/man/man1
mv mplayer.1 mplayer2.1

# nroff does not understand macros used by mplayer man page
# See http://www.mplayerhq.hu/DOCS/tech/manpage.txt
#mkdir %buildroot/%_datadir/man/cat1
#cd %buildroot/%_datadir/man/cat1
cd ..
mkdir cat1
groff -mman -Tutf8 -rLL=78n man1/mplayer2.1 | col -bxp > cat1/mplayer2.1

rm -rf %buildroot/%_libdir
rm -rf %buildroot/%_sysconfdir

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir/*
%dir %attr (0755, root, sys) %_datadir
%_mandir/man1
%_mandir/cat1
%_datadir/mplayer2/subfont.ttf


%changelog
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
