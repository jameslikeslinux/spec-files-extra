#
# spec file for package SFEstellarium
#
# includes module(s): stellarium
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

### NOTE ### (Alex Viskovatoff)
###
### The only way I can get this to link successfully is to remove
### libgcc_s.so* and libstdc++.* from /usr/sfw/lib while building.

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc

Name:		SFEstellarium
Version:	0.11.0
Summary:	Photo-realistic night sky renderer
Group:		Applications/Games
License:	GPLv2+
SUNW_Copyright:	stellarium.copyright
URL:		http://stellarium.free.fr/
Source:		%{sf_download}/stellarium/stellarium-%{version}.tar.gz
#Patch1:		stellarium-01-sunstudio.diff
Patch2:		stellarium-02-gcc-name-conflict.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer
#BuildRequires: SUNWimagick
BuildRequires: SFEcmake
BuildRequires: SFEqt47-gpp-devel
Requires: SFEqt47-gpp

%description
Stellarium is a real-time 3D photo-realistic nightsky renderer. It can
generate images of the sky as seen through the Earth's atmosphere with
more than one hundred thousand stars from the Hipparcos Catalogue,
constellations, planets, major satellites and nebulas.

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n stellarium-%{version}
#%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# pod2man
export CC=/usr/gnu/bin/cc
export CXX=/usr/gnu/bin/g++
export PATH=/usr/g++/bin:$PATH:/usr/perl5/bin
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -D__C99FEATURES__"
export LDFLAGS="%_ldflags"
export QMAKESPEC=solaris-g++

mkdir -p builds/unix
cd builds/unix

cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DCMAKE_LIBRARY_PATH=/usr/gnu/lib:/usr/g++/lib ../..
#make VERBOSE=1 -j$CPUS
make -j$CPUS
cd ../..
convert -size 32x32 data/icon.bmp stellarium.png

%install
rm -rf %{buildroot}
cd builds/unix
make install DESTDIR=%{buildroot} INSTALL="%{_bindir}/ginstall -c -p"
cd ../..

# Setting CMAKE_LIBRARY_PATH does not do any good
elfedit -e 'dyn:runpath /usr/gnu/lib:/usr/g++/lib' %buildroot/%_bindir/stellarium

mkdir -p %{buildroot}%{_datadir}/pixmaps/
ginstall -m 0644 -p data/stellarium.png %{buildroot}%{_datadir}/pixmaps/stellarium.png

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf %{buildroot}%{_datadir}/locale
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/stellarium
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/stellarium.png
%{_mandir}/man1/stellarium.1

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 0.11.0
* Fri Jul 29 2011 - Alex Viskovatoff
- add SUNW_Copyright
* Sat Jul 02 2011 - Alex Viskovatoff
- fork new spec using gcc to build off SFEstellarium.spec
* Mon Mar 07 2011 - Alex Viskovatoff
- use SFEcmake; boost is not a dependency
* Tue Feb 08 2011 - Milan Jurik
- initial spec
