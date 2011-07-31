#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

Summary:                 A very fast video and audio converter
Version:                 0.8
Source:                  http://www.ffmpeg.org/releases/ffmpeg-%version.tar.bz2
URL:                     http://www.ffmpeg.org/index.html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%prep
%setup -q -n ffmpeg-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
# for pod2man
export PATH=/usr/perl5/bin:$PATH
export CC=/usr/gnu/bin/gcc
# All this is necessary to free up enough registers on x86
%ifarch i386
export CFLAGS="%optflags -Os -fno-rename-registers -fomit-frame-pointer -fno-PIC -UPIC -mpreferred-stack-boundary=4 -I%{xorg_inc} -I%{_includedir}"
%else
export CFLAGS="%optflags -Os -I%{xorg_inc} -I%{_includedir}"
%endif
#export LDFLAGS="%_ldflags %{xorg_lib_path} -L/usr/sfw/lib -R/usr/sfw/lib -L%{_libdir} -R%{_libdir}"
export LDFLAGS="%_ldflags %{xorg_lib_path} -L%{_libdir} -R%{_libdir}"
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
    --extra-ldflags=-mimpure-text \
    --enable-shared

gmake 

%install
gmake install DESTDIR=$RPM_BUILD_ROOT BINDIR=$RPM_BUILD_ROOT%{_bindir}

mkdir $RPM_BUILD_ROOT%{_libdir}/ffmpeg
cp config.mak $RPM_BUILD_ROOT%{_libdir}/ffmpeg

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
