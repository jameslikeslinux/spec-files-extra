#
# spec file for package: murrine-engine
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%define src_name murrine

Name:		murrine-engine
Version:	0.98.1.1
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{src_name}/0.98/%{src_name}-%{version}.tar.bz2
Source1:	http://www.cimitan.com/murrine/files/MurrinaGilouche.tar.bz2
Source2:	http://www.cimitan.com/murrine/files/MurrinaAquaIsh.tar.bz2
Source3:	http://www.cimitan.com/murrine/files/MurrinaVerdeOlivo.tar.bz2
Source4:	http://www.cimitan.com/murrine/files/MurrinaFancyCandy.tar.bz2
Source5:	http://www.cimitan.com/murrine/files/MurrinaLoveGray.tar.bz2
Source6:	http://www.cimitan.com/murrine/files/MurrineRounded.tar.bz2
Patch0:		murrine-engine-01-pixman-libs.diff

%prep
%setup -q -n %{src_name}-%{version}

# Fix autotools for libpixman dependency
%patch0 -p1
aclocal
autoconf
libtoolize --force
automake

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
export PKG_CONFIG_LIBDIR="%{_libdir}/pkgconfig:/usr/share/pkgconfig"
./configure --prefix=%{_prefix} --libdir=%{_libdir} --enable-animation
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/*.la
mkdir -p $RPM_BUILD_ROOT%{_datadir}/themes
gtar -xvjf %{SOURCE1} -C $RPM_BUILD_ROOT%{_datadir}/themes
gtar -xvjf %{SOURCE2} -C $RPM_BUILD_ROOT%{_datadir}/themes
gtar -xvjf %{SOURCE3} -C $RPM_BUILD_ROOT%{_datadir}/themes
gtar -xvjf %{SOURCE4} -C $RPM_BUILD_ROOT%{_datadir}/themes
gtar -xvjf %{SOURCE5} -C $RPM_BUILD_ROOT%{_datadir}/themes
gtar -xvjf %{SOURCE6} -C $RPM_BUILD_ROOT%{_datadir}/themes

%clean
rm -rf $RPM_BUILD_ROOT
