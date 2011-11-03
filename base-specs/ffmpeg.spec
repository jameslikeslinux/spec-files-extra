#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

Summary:                 A very fast video and audio converter
Version:                 0.8.5
Source:                  http://www.ffmpeg.org/releases/ffmpeg-%version.tar.bz2
URL:                     http://www.ffmpeg.org/index.html
Patch9:			 ffmpeg-09-configure-gnuism-pod2man.diff
Patch10:		 ffmpeg-10-Makefile-quick-texi2html-fix.diff
Patch11:		 ffmpeg-11-add-sys_videodev2_h.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%prep
%setup -q -n ffmpeg-%version
%patch9 -p1
%patch10 -p1
%patch11 -p1
perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," `find . -type f -exec grep -q "^#\!.*/bin/sh" {} \; -print`



%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
# for pod2man
export PATH=/usr/perl5/bin:$PATH
export CC=gcc
# All this is necessary to free up enough registers on x86
%ifarch i386
export CFLAGS="%optflags -Os %{extra_gcc_flags} -fno-rename-registers -fomit-frame-pointer -fno-PIC -UPIC -mpreferred-stack-boundary=4 -I%{xorg_inc} -I%{_includedir}"
%else
export CFLAGS="%optflags -Os %{extra_gcc_flags} -I%{xorg_inc} -I%{_includedir}"
%endif
export LDFLAGS="%_ldflags %{xorg_lib_path}"
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export LDFLAGS="$LDFLAGS -m64"
fi
bash ./configure	\
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir}	\
    --shlibdir=%{_libdir}	\
    --mandir=%{_mandir}	\
    --cc=$CC		\
    %{arch_opt}		\
    --disable-debug	\
    --enable-nonfree	\
    --enable-gpl	\
    --enable-postproc	\
    --enable-avfilter   \
    --enable-swscale	\
    --enable-libgsm	\
    --enable-libxvid	\
    --enable-libx264	\
    --enable-libfaac	\
    --enable-libtheora	\
    --enable-libmp3lame	\
    --enable-libvorbis	\
    --enable-libvpx	\
    --enable-x11grab	\
    --enable-libspeex   \
    --enable-pthreads	\
    --enable-libopencore-amrnb \
    --enable-libopencore-amrwb \
    --enable-version3 \
    --disable-static	\
    --disable-mlib	\
    --enable-libschroedinger \
    --enable-libopenjpeg \
    --enable-librtmp \
    --enable-vdpau	\
    --enable-shared

gmake -j$CPUS

%install
# for pod2man
export PATH=/usr/perl5/bin:$PATH
gmake install DESTDIR=$RPM_BUILD_ROOT BINDIR=$RPM_BUILD_ROOT%{_bindir}

mkdir $RPM_BUILD_ROOT%{_libdir}/ffmpeg
cp config.mak $RPM_BUILD_ROOT%{_libdir}/ffmpeg

#workaround for occasional not finding of %doc files
touch placeholder.html
cp -p *.html doc/
mkdir -p %buildroot%_docdir/ffmpeg
cp -p doc/developer.html doc/faq.html doc/ffmpeg.html doc/ffplay.html doc/ffprobe.html doc/ffserver.html doc/general.html doc/libavfilter.html %buildroot%_docdir/ffmpeg

# Create a ffmpeg.pc - Some apps need it
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/ffmpeg.pc << EOM
Name: ffmpeg
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include
Description: FFmpeg codec library
Version: 51.40.4
Requires:  libavcodec libpostproc libavutil libavformat libswscale x264 ogg theora vorbisenc vorbis dts
Conflicts:
EOM

#mv $RPM_BUILD_ROOT%{_libdir}/lib*.*a $RPM_BUILD_ROOT%{_libdir}/ffmpeg

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Nov  1 2011 - Alex Viskovatoff
- enable libvpx
* Sun Oct 23 2011 - Alex Viskovatoff
- remove --extra-ldflags=-mimpure-text
* Wed Oct 12 2011 - Alex Viskovatoff
- bump to 0.8.5; enable librtmp; do not hardcode path of gcc
* Wed Aug 17 2011 - Thomas Wagner
- %arch_sse2 change minimum-CPU i686 to prescott, add --enable-sse --enable-ssse2
- for arch i86 by default --enable-runtime-cpudetect, add extra_gcc_flags -msse
  to have asm being lucky with XMM_CLOBBERS, remove --disable-asm (asm active again)
- remove build-time pkgtool commandline option --with-runtime_cpudetect (now 
  always enabled for i86)
- Implementation note: Programs using pentium_pro+mmx must request these libs 
  with isaexec (see what ffmpeg binary does via /usr/lib/isaexec) or in other
  progams tell the linker to select the library for you, via 
  export LD_OPTIONS='-f libavcodec.so.53:libavdevice.so.53:libavfilter.so.2:
  libavformat.so.53:libavutil.so.51:libswscale.so.2:libpostproc.so.51'
  and -R this early in LD_FLAGS="-R%{_libdir}/\$ISALIST %_ldflags"
  At least put ISALIST before any other -R/usr/lib !
  For debug use       LD_DEBUG=libs program_to_test
* Sat Aug 13 2011 - Thomas Wagner
- bump to 0.8.2
- change in include/x86_sse2.inc to not set -xarch=sse2 in arch_ldadd 
  for case cc_is_gcc == 1 - this avoids gcc errors in configure
  "gcc: error: language arch=sse2 not recognized"
- add switch with_runtime_cpudetect, by default set to off 
  (Distro builders may switch this to on with pkgtool --with-runtime_cpudetect )
##TODO## might need some testing if acceleration works on CPUs
- comment %doc, manpages - files not present in 0.8.2
- re-add patches removed with r3618, reworked,
  patch9: configure gnuism, re-add manpages by pod2man if texi2html not available,
  (reworked ffmpeg-02-configure.diff and ffmpeg-03-gnuisms.diff)
  patch10: *new* get texi2html work again - fix probably incomplete or needs updated
  texi2html, re-add %doc and manpages
- allow parallel build gmake -j$CPUS
- add patch11: ffmpeg-11-add-sys_videodev2_h.diff (reworked ffmpeg-03-v4l2.diff)
##TODO## v4l2 patch11 incomplete, maybe needs more from ffmpeg-03-v4l2.diff, ffmpeg-07-new-v4l2.diff
- for pod2man add in %install export PATH=/usr/perl5/bin:$PATH
- fix perms for %{_datadir}/doc
- replace %doc with manual install
- make all /bin/sh script in source tree use /usr/bin/bash
##TODO## patch11 incomplete, maybe needs more from ffmpeg-03-v4l2.diff, ffmpeg-07-new-v4l2.diff
##TODO## verify build-time dependencies (texi2html, pod2man, others)
##TODO## check if v4l patches still apply on Solaris
* Tue Aug  9 2011 - Alex Viskovatoff
- add --enable-vdpau, which can speed up decoding
* Fri Jul 29 2011 - Alex Viskovatoff
- add --enable-version3 option to keep build from failing
* Sun Jul 17 2011 - Alex Viskovatoff
- update to 0.8, discarding all patches (all fail and apparently are superfluous)
- remove obsolete flags from invocation of ./configure
* Wed May 11 2011 - Alex Viskovatoff
- bump to 0.6.3
* Thu Apr 27 2011 - Alex Viskovatoff
- remove superflous macro src_version
* Sat Mar 26 2011 - Milan Jurik
- bump to 0.6.2
* Wed Jan 05 2011 - James Choi <jchoi42@pha.jhu.edu>
- patch configure to gnu defaults
* Sun Nov 28 2010 - Milan Jurik
- bump to 0.6.1
* Wed Jun 16 2010 - Milan Jurik
- update to 0.6
- remove older amr codecs, add libschroedinger and openjpeg
- remove mlib because it is broken now
- remove Solaris V4L2 support, more work needed 
* Fri Jun 11 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.5.2
- Update URLs
- Use -Os to avoid H.264 decoder crash
* Mar 12 2010 - Gilles Dauphin
- in case of prefix=/usr/SFE
* Sun Mar 07 2010 - Milan Jurik
- replace amrXX for opencore implementation
* Wed Mar 03 2010 - Milan Jurik
- update to 0.5.1
* Sat Oct 17 2009 - Milan Jurik
- svn branch 0.5 patch added (2009-07-05)
* Tue Sep 08 2009 - Milan Jurik
- support for newer gcc if installed
* Sun Jun 28 2009 - Milan Jurik
- switch to GNU make
* Mon Mar 16 2009 - Milan Jurik
- version 0.5
* Thu Aug 07 2008 - trisk@acm.jhu.edu
- Add patch6, update CFLAGS
* Thu Mar 27 2008 - trisk@acm.jhu.edu
- Convert to base-spec
- Update to 0.4.9-p20080326 from electricsheep.org
- Update patches
- Disable static libs
* Mon Jun 30 2008 - andras.barna@gmail.com
- Force SFWgcc
- Add -I/usr/X11/include
* Tue Mar 18 2008 - trisk@acm.jhu.edu
- Add patch5 to fix green tint with mediaLib, contributed by James Cheng
* Sat Aug 11 2007 - trisk@acm.jhu.edu
- Disable mediaLib support on non-sparc (conflicts with MMX)
- Enable x11grab for X11 recording
- Enable v4l2 demuxer for video capture
- Add workaround for options crash
* Wed Aug  3 2007 - dougs@truemail.co.th
- Bumped export version
- Added codecs
- Created ffmpeg.pc
* Tue Jul 31 2007 - dougs@truemail.co.th
- Added SUNWlibsdl test. Otherwise require SFEsdl
* Sat Jul 14 2007 - dougs@truemail.co.th
- Build shared library
* Sun Jan 21 2007 - laca@sun.com
- fix devel pkg default attributes
* Wed Jan 10 2007 - laca@sun.com
- create
