#
# spec file for package SFElibx264
#
# includes module(s): libx264
#

##TODO##  Make x264 executable link to SFEffmpeg

# libx264 complains on yasm too old, just uninstall
# the one you got with the CBE 1.6.x or 1.7.x release
# pfexec pkgrm CBEyasm
#The following package is currently installed:
#   CBEyasm  Desktop CBE: Yet another assembler
#            (i386) 0.6.2,REV=1.7.0
#Do you want to remove this package? [y,n,?,q] y

#or

#pfexec pkg uninstall CBEyasm


%include Solaris.inc

%define cc_is_gcc 1 
%ifarch amd64 sparcv9
%include arch64.inc
%use libx264_64 = libx264.spec
%endif

%include base.inc
%use libx264 = libx264.spec

%define with_gpac %(pkginfo -q SFEgpac && echo 1 || echo 0)

Name:                    SFElibx264
IPS_Package_Name:	library/video/x264 
Summary:                 %{libx264.summary}
Group:                   System/Multimedia Libraries
License:                 GPLv2
SUNW_Copyright:	         libx264.copyright
URL:                     http://www.videolan.org/developers/x264.html
Version:                 %{libx264.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%define SFEmpfr         %(/usr/bin/pkginfo -q SFEmpfr 2>/dev/null  && echo 1 || echo 0)

%if %SFEmpfr
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
#workaround on IPS which is wrong with BASEdir as "/" -> then assume /usr/gnu
%define SFEmpfrbasedir %(pkgparam SFEmpfr BASEDIR 2>/dev/null | sed -e 's+^/$+/usr/gnu+')
%else
BuildRequires: SUNWgnu-mpfr
Requires: SUNWgnu-mpfr
%endif

%ifarch i386 amd64
BuildRequires: SFEyasm
%endif

%if %with_gpac
BuildRequires: SFEgpac-devel
Requires: SFEgpac
%endif

BuildRequires: SUNWgawk

%description
x264 is a free software library and application for encoding video streams into
the H.264/MPEG-4 AVC format.

Encoder features:

    * 8x8 and 4x4 adaptive spatial transform
    * Adaptive B-frame placement
    * B-frames as references / arbitrary frame order
    * CAVLC/CABAC entropy coding
    * Custom quantization matrices
    * Intra: all macroblock types (16x16, 8x8, 4x4, and PCM with all predictions)
    * Inter P: all partitions (from 16x16 down to 4x4)
    * Inter B: partitions from 16x16 down to 8x8 (including skip/direct)
    * Interlacing (MBAFF)
    * Multiple reference frames
    * Ratecontrol: constant quantizer, constant quality, single or multipass ABR, optional VBV
    * Scenecut detection
    * Spatial and temporal direct mode in B-frames, adaptive mode selection
    * Parallel encoding on multiple CPUs
    * Predictive lossless mode
    * Psy optimizations for detail retention (adaptive quantization, psy-RD, psy-trellis)
    * Zones for arbitrarily adjusting bitrate distribution


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libx264_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libx264.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
%libx264_64.build -d %name-%version/%_arch64
%endif

%libx264.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libx264_64.install -d %name-%version/%_arch64
%endif

%libx264.install -d %name-%version/%{base_arch}
find $RPM_BUILD_ROOT%{_libdir} -name \*.la -exec rm {} \;
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/x264  $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
cd $RPM_BUILD_ROOT%{_bindir} && cp -p /usr/lib/isaexec x264
#cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec x264


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/*
%endif
%{_bindir}/%{base_isa}/*
%{_bindir}/x264
#%hard %{_bindir}/x264
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif


%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif


%changelog
* Thu Jun 21 2012 - Logan Bruns <logan@gedanken.org>
- autodetect whether to use SFEmpfr or system provided version.
* Fri Oct 21 2011 - Milan Jurik
- autodetect gpac
* Sun Oct 16 2011 - Milan Jurik
- add IPS package name, keep SFEgpac as mandatory
* Wed Oct 12 2011 - Alex Viskovatoff
- Add new build dependency on library/mpfr
* Thu Jul 21 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Wed Nov 10 2010 - Alex Viskovatoff
- add optional (Build)Requires: SFEgpac(-devel)
* Fri Apr 09 - Milan Jurik
- yasm is only for x86, not SPARC
* Mar 2010 - Gilles Dauphin
- because of install could be in /usr/SFE/bin we cp isaexec
- instead of hardlink it
* Sat Nov 28 2009 - Albert Lee <trisk@opensolaris.org>
- Remove GPAC dependency
* Tue Sep 8 2009 - Milan Jurik
- multiarch support
* Mon Mar 16 2009 - andras.barna@gmail.com
- Add patch7
* Sun Mar 15 2009 - Milan Jurik
- the latest snapshot
* Mon Jun 30 2008 - andras.barna@gmail.com
- Force SFWgcc
* Fri May 23 2008 - michal.bielicki <at> voiceworks.pl
- h26x chokes on optflags, fix by Giles Dauphin
* tue Jan 08 2008 - moinak.ghosh@sun.com
- Build with gcc and enable C99FEATURES.
* Tue Nov 20 2007 - daymobrew@users.sourceforge.net
- Bump to 20071119 and add Url.
* Sun Aug 12 2007 - dougs@truemail.co.th
- Added SFEgpac as Required
* Fri Aug  3 2007 - dougs@truemail.co.th
- initial version
