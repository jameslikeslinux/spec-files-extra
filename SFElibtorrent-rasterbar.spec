#
# spec file for package SFElibtorrent-rasterbar
#
# includes module: libtorrent-rasterbar
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define _prefix %_basedir/g++
%define srcname libtorrent-rasterbar

Name:		SFElibtorrent-rasterbar
IPS_package_name: library/g++/libtorrent-rasterbar
Summary:	Feature complete C++ bittorrent implementation focusing on efficiency and scalability
Group:		System/Libraries
URL:		http://www.rasterbar.com/products/libtorrent/
Meta(info.upstream):	Arvid Norberg <arvid@rasterbar.com>
Version:	0.15.8
License:	BSD with advertising
SUNW_copyright:	%srcname.copyright
Source:		http://libtorrent.googlecode.com/files/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%srcname-%version-build
%include default-depend.inc


%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name

BuildRequires:	SFEgcc
Requires:	SFEgccruntime
BuildRequires:	SFEboost-gpp-devel
Requires:	SFEboost-gpp
BuildRequires:	SFEgeoip-devel
Requires:	SFEgeoip


%prep
%setup -q -n %srcname-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CPPFLAGS="-pthreads -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -pthreads -lxnet -L/usr/g++/lib -R/usr/g++/lib"

./configure --prefix=%_prefix --bindir=%_basedir/bin --libdir=%_libdir --with-boost=/usr/g++ --disable-static --with-libgeoip --enable-examples

gmake -j$CPUS

%install
rm -rf %buildroot
gmake install DESTDIR=%buildroot
rm %buildroot%_libdir/*.la

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_libdir/lib*.so*
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/*
%_basedir/bin

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %_includedir/libtorrent
%_includedir/libtorrent/*


%changelog
* Thu Oct 27 2011 - Alex Viskovatoff
- Bump to 0.15.8; add SUNW_copyright and IPS_package_name
* Mon Aug 29 2011 - Alex Viskovatoff
- Build examples
* Sun Aug 28 2011 - Alex Viskovatoff
- Build with gcc
* Tue Jan 18 2011 - Alex Viskovatoff
- Initial spec
