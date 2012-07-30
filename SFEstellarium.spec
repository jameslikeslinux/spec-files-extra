#
# spec file for package SFEstellarium
#
# includes module(s): stellarium
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include stdcxx.inc

Name:		SFEstellarium
IPS_Package_Name:	image/stellarium
Version:	0.11.3
Summary:	Photo-realistic nightsky renderer
Group:		Amusements/Graphics
License:	GPLv2+
URL:		http://stellarium.free.fr/
Source:		%{sf_download}/stellarium/stellarium-%{version}.tar.gz
Patch1:		stellarium-01-studio.diff
SUNW_Copyright:	stellarium.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer
BuildRequires: SUNWimagick
BuildRequires: SFEcmake
BuildRequires: SFEqt-stdcxx-devel
Requires: SFEqt-stdcxx

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
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# pod2man
export PATH=/usr/stdcxx/bin:$PATH:/usr/perl5/bin:
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -library=no%Cstd -I%{stdcxx_include} -I/usr/stdcxx/include"
export LDFLAGS="%_ldflags -L%{stdcxx_lib} -R%{stdcxx_lib} -L/usr/stdcxx/lib -R/usr/stdcxx/lib -lstdcxx4 -Wl,-zmuldefs"

mkdir -p builds/unix
cd builds/unix

cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ../..
make VERBOSE=1 -j$CPUS
cd ../..
convert -size 32x32 data/icon.bmp stellarium.png

%install
rm -rf %{buildroot}
cd builds/unix
make install DESTDIR=%{buildroot} INSTALL="%{_bindir}/ginstall -c -p"
# TODO: find solution for stripping RUNPATH
cp src/stellarium %{buildroot}%{_bindir}/stellarium
cd ../..

mkdir -p %{buildroot}%{_datadir}/pixmaps/
install -m 0644 -p stellarium.png %{buildroot}%{_datadir}/pixmaps/stellarium.png

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
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/stellarium.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/stellarium.png
%{_datadir}/pixmaps/stellarium.xpm
%{_mandir}/man1/stellarium.1

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Jul 29 2012 - Milan Jurik
- bump to 0.11.3
* Sun Jan 08 2012 - Milan Jurik
- bump to 0.11.1, fix qt-stdcxx
* Thu Sep 1 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 0.11.0
- Created stellarium-0.11.0-01-sunstudio.diff for 0.11.0
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Mon Mar  7 2011 - Alex Viskovatoff
- use SFEcmake; boost is not a dependency
* Tue Feb 08 2011 - Milan Jurik
- initial spec
