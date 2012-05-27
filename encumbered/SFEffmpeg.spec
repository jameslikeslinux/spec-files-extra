#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%if %arch_sse2
#%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2 --enable-sse --enable-sse
%define arch_opt --cpu=prescott --enable-mmx --enable-mmx2 --enable-sse --enable-ssse3
#make this empty
%define extra_gcc_flags
%include x86_sse2.inc
%use ffmpeg_sse2 = ffmpeg.spec
%endif

%ifarch sparc
%define arch_opt --disable-optimizations
%endif

%ifarch i386
#with -msse (gcc) you can have asm XMM_CLOBBERS accepted
#read line 00079 in http://www.libav.org/doxygen/master/x86__cpu_8h_source.html 
%define extra_gcc_flags -msse
%define arch_opt --enable-runtime-cpudetect --enable-mmx --enable-mmx2 --enable-sse --enable-ssse3 
%endif

%include base.inc
%use ffmpeg = ffmpeg.spec

Name:                    SFEffmpeg
IPS_Package_Name:	video/ffmpeg
Summary:                 %{ffmpeg.summary}
Version:                 %{ffmpeg.version}
License:                 GPLv2+ and LGPLv2.1+
SUNW_Copyright:          ffmpeg.copyright
URL:                     %{ffmpeg.url}
Group:		         System/Multimedia Libraries

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%include default-depend.inc
BuildRequires: SFEgcc
Requires:      SFEgccruntime
BuildRequires: SFEyasm
BuildRequires: SUNWtexi
BuildRequires: %pnm_buildrequires_perl_default
BuildRequires: SUNWxwinc
Requires: SUNWxwrtl
Requires: SUNWzlib
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
BuildRequires: SFElibgsm-devel
Requires: SFElibgsm
BuildRequires: SFExvid-devel
Requires: SFExvid
BuildRequires: SFElibx264-devel
Requires: SFElibx264
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
BuildRequires: SFEfaac-devel
Requires: SFEfaac
BuildRequires: SFElame-devel
Requires: SFElame
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWlibtheora-devel
Requires: SUNWlibtheora
BuildRequires: SUNWspeex-devel
Requires: SUNWspeex
BuildRequires: SFEopencore-amr-devel
Requires: SFEopencore-amr
BuildRequires: SUNWgsed
BuildRequires: SFEopenjpeg-devel
Requires: SFEopenjpeg
BuildRequires: SFElibschroedinger-devel
Requires: SFElibschroedinger
BuildRequires: SFErtmpdump-devel
Requires: SFErtmpdump
BuildRequires: SFElibass-devel
Requires: SFElibass
BuildRequires: SFEopenal-devel
Requires: SFEopenal
BuildRequires: SFElibvpx-devel
Requires: SFElibvpx

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%ffmpeg_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%ffmpeg.prep -d %name-%version/%base_arch


%build
%if %arch_sse2
%ffmpeg_sse2.build -d %name-%version/%sse2_arch
%endif

%ffmpeg.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT

%if %arch_sse2
%ffmpeg_sse2.install -d %name-%version/%sse2_arch
%endif

%ffmpeg.install -d %name-%version/%base_arch
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/ffserver $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec ffserver
mv $RPM_BUILD_ROOT%{_bindir}/ffplay $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec ffplay
mv $RPM_BUILD_ROOT%{_bindir}/ffmpeg $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec ffmpeg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%define _pkg_docdir %_docdir/ffmpeg
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{base_isa}/*
%if %arch_sse2
%{_bindir}/%{sse2_arch}/*
%endif
%hard %{_bindir}/ffserver
%hard %{_bindir}/ffplay
%hard %{_bindir}/ffmpeg
%hard %{_bindir}/ffprobe
#%hard %{_bindir}/avconv
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%if %arch_sse2
%dir %attr (0755, root, bin) %{_libdir}/%{sse2_arch}
%{_libdir}/%{sse2_arch}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/ffmpeg
%{_mandir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%if %arch_sse2
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
%endif
%{_libdir}/ffmpeg
%if %arch_sse2
%{_libdir}/%{sse2_arch}/ffmpeg
%endif
%{_includedir}


%changelog
* Sun May 27 2012 - Milan Jurik
- bump to 0.11
* Sun Apr 29 2012 - Pavel Heimlich
- really add vpx dependency
* Tue Jan 24 2012 - James Choi
- update files for 0.10
* Mon Dec 12 2011 - Milan Jurik
- bump to 0.9
* Sun Nov 13 2011 - Michael Kosarev
- add libvpx dependency
* Sun Oct 23 2011 - Milan Jurik
- add IPS package name
- add rtmp dep
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
* Sat Jul 16 2011 - Alex Viskovatoff
- Add SFEyasm as a dependency; package documentation files
- Add --disable-asm as option for i386 so that newer versions build
* Wed May 11 2011 - Alex Viskovatoff
- Add SFEgccruntime as a dependency
* Mon Jan 24 2011 - Alex Viskovatoff
- Add missing build dependency
* Wed Jun 16 2010 - Milan Jurik
- update to 0.6
- remove older amr codecs, add libschroedinger and openjpeg
- remove mlib because it is broken now
- remove Solaris V4L2 support, more work needed
* Tue Apr 06 2010 - Milan Jurik
- missing perl build dependency (pod2man)
* Sun Mar 07 2010 - Milan Jurik
- replace amrXX for opencore implementation
* Tue Sep 08 2009 - Milan Jurik
- amrXX optional
- improved multiarch support (64-bit not done because of missing SUNW libraries)
* Mon Mar 16 2009 - Milan Jurik
- version 0.5
* Fri Jun 13 2008 - trisk@acm.jhu.edu
- New spec for base-spec
