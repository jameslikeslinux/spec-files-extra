#
# spec file for package SFElibmaa
#
# includes module: libass
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname libass

Name:		SFElibass
Summary:	Portable renderer for the ASS/SSA (Substation Alpha) subtitle format
Group:		System/Multimedia Libraries
URL:		http://code.google.com/p/libass/
Version:	0.9.12
License:	BSD
Source:		http://%srcname.googlecode.com/files/%srcname-%version.tar.xz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

# Copied from Wikipedia
%description
SubStation Alpha (or Sub Station Alpha), abbreviated SSA, is a subtitle file
format created by CS Low (also known as Kotus) that allows for more advanced
subtitles than the conventional SRT and similar formats. This format can be
rendered with VSFilter in conjunction with a DirectShow-aware video player
(on Microsoft Windows), or MPlayer with the SSA/ASS library.

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=/usr/gnu/bin/gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%_prefix
gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_libdir/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_libdir
%_libdir/%srcname.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%srcname.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/ass


%changelog
* Sat Jul 16 2011 - Alex Viskovatoff
- Initial spec
