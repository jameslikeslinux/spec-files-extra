#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%define with_runtime_cpudetect 1

%define SUNWlibsdl %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%ifarch sparc
%define arch_opt --disable-optimizations
%endif

%ifarch i386
%define arch_opt --cpu=prescott --enable-runtime-cpudetect --enable-mmx --enable-mmx2 --enable-sse --enable-ssse3
%define extra_gcc_flags
%endif

%use ffmpeg = ffmpeg.spec

Name:                    SFEffmpeg
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
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
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
BuildRequires: driver/graphics/nvidia
#Requires: driver/graphics/nvidia

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%ffmpeg.prep -d %name-%version/%base_arch


%build
%ffmpeg.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT

%ffmpeg.install -d %name-%version/%base_arch
mkdir %buildroot%_docdir

%clean
rm -rf $RPM_BUILD_ROOT


%files
%define _pkg_docdir %_docdir/ffmpeg
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/ffmpeg
%{_datadir}/ffmpeg/*.ffpreset
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %dir %_docdir
%doc -d %base_arch/ffmpeg-%version/doc developer.html faq.html ffmpeg.html ffplay.html ffprobe.html ffserver.html general.html libavfilter.html

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/ffmpeg
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libavutil
%{_includedir}/libavcodec
%{_includedir}/libavfilter
%{_includedir}/libavformat
%{_includedir}/libavdevice
%{_includedir}/libpostproc
%{_includedir}/libswscale


%changelog
* Tue Aug  9 2011 - Alex Viskovatoff
- Require driver/graphics/nvidia; correct attributes of %_docdir
* Mon Jul 18 2011 - Alex Viskovatoff
- Do not use x86_sse2.inc: it adds Sun Studio-specific flags
* Sat Jul 16 2011 - Alex Viskovatoff
- Fork new spec off SFEffmpeg.spec with multiarch support (CPU < SSE2) removed
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
