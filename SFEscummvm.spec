#
# spec file for package SFEscummvm
#
# includes module(s): ScummVM
#
%include Solaris.inc

%define with_libmad %(pkginfo -q SFElibmad && echo 1 || echo 0)

Name:                    SFEscummvm
IPS_Package_Name:	games/scummvm
Summary:                 ScummVM - emulator for classic graphical games
Version:                 1.4.1
Group:                   System/Emulators/Other
Source:                  %{sf_download}/scummvm/scummvm-%{version}.tar.bz2
URL:                     http://www.scummvm.org/
License:                 GPLv2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
BuildRequires: SUNWzlib
Requires: SUNWzlib
BuildRequires: SUNWflac-devel
Requires: SUNWflac
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SFEfluidsynth-devel
Requires: SFEfluidsynth
%if %with_libmad
BuildRequires: SFElibmad-devel
Requires: SFElibmad
%endif
%ifarch i386 amd64
BuildRequires: SFEnasm
%endif

%prep
%setup -q -n scummvm-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%gcc_optflags -I/usr/sfw/include -DANSICPP -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export CPPFLAGS="-I/usr/sfw/include -I%{_includedir}"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -L%{_libdir} -R%{_libdir}"
export MSGFMT="/usr/bin/msgfmt"
export CXX=/usr/sfw/bin/gcc
export CC=/usr/sfw/bin/gcc
export PATH=$PATH:/usr/ccs/bin

./configure --prefix=%{_prefix}		\
            --mandir=%{_mandir}		\
            --enable-all-engines	\
            --enable-plugins		\
            --enable-release

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/scummvm.desktop << EOF
[Desktop Entry]
Name=ScummVM
Comment=Emulator for classic graphical games
Exec=%{_bindir}/scummvm
Icon=scummvm
Terminal=false
Type=Application
Categories=Game;
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/scummvm.desktop
%dir %attr (0755, root, other) %{_datadir}/scummvm
%{_datadir}/scummvm/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_mandir}

%changelog
* Tue Feb 07 2012 - Milan Jurik
- bump to 1.4.1
* Sat Nov 19 2011 - Milan Jurik
- menu entry
* Mon Sep 19 2011 - Milan Jurik
- bump to 1.3.1
* Thu Dec 16 2010 - Milan Jurik
- bump to 1.2.1
* Wed Dec 01 2010 - Milan Jurik
- bump to 1.2.0
* Mon Aug 30 2010 - Milan Jurik
- bump to 1.1.1
* May 02 2010 - Gilles Dauphin
- search in %{_basedir} if in /opt/SFE (ligmpeg2 is in)
* Fri Apr 30 2010 - Milan Jurik
- fix SPARC build
* Thu Apr 29 2010 - Milan Jurik
- update to 1.1.0
* Sat Jan 16 2009 - Milan Jurik
- update to 1.0.0
* Sat Nov 17 2007 - trisk@acm.jhu.edu
- Bump to 0.10.0
* Fri Jul  7 2006 - laca@sun.com
- rename to SFEscummvm
- bump to 0.9.0
- update file attributes
- delete patchb build-fix.diff, no longer needed
* Wed Nov 09 2005 - glynn.foster@sun.com
- Initial spec
