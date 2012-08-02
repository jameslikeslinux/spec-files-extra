#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libsamplerate64 = libsamplerate.spec
%endif

%include base.inc
%use libsamplerate = libsamplerate.spec

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:                SFElibsamplerate
IPS_Package_Name:    library/audio/libsamplerate
Summary:             %{libsamplerate.summary}
URL:                 http://www.mega-nerd.com/SRC/
Meta(info.upstream): Erik de Castro Lopo <erikd@mega-nerd.com>
License:             GPLv2
SUNW_Copyright:	     libsamplerate.copyright
Version:             %{libsamplerate.version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:  SUNWaudh
#if build, examples will require libsndfile
%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%description
Secret Rabbit Code (aka libsamplerate) is a Sample Rate Converter for audio. One
example of where such a thing would be useful is converting audio from the CD
sample rate of 44.1kHz to the 48kHz sample rate used by DAT players.

SRC is capable of arbitrary and time varying conversions; from downsampling by
a factor of 256 to upsampling by the same factor. Arbitrary in this case means
that the ratio of input and output sample rates can be an irrational number. The
conversion ratio can also vary with time for speeding up and slowing down
effects.

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libsamplerate64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libsamplerate.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libsamplerate64.build -d %name-%version/%_arch64
%endif

%libsamplerate.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libsamplerate64.install -d %name-%version/%_arch64
%endif

%libsamplerate.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sndfile-resample
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/sndfile-resample
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Fri Jun 22 2012 - Logan Bruns <logan@gedanken.org>
- added ips package name.
* Thu Jul 21 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Thu Feb 04 2010 - Halton Huo <halton.huo@gmail.com>
- Add SUNWaudioh as BuildRequires
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Thu Sep 06 2007 - Thomas Wagner
- (Build)Requires on SFElibsndfile(-devel)
* Sun Aug 12 2007 - dougs@truemail.co.th
- Changed to build 64bit
* 20070522 Thomas Wagner
- Initial spec
