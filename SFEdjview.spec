#
# spec file for package SFEdjview
#
# includes module: djview
#

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define  _cxx_libdir /usr/g++/lib
%define srcname djview

Name:		SFEdjview
Summary:	DjVu file viewer
URL:		http://djvu.sourceforge
Vendor:		Léon Bottou
License:	GPLv2+
SUNW_Copyright:	djview.copyright
Version:	4.7
Source:		%sf_download/project/djvu/DjView/%version/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEgcc
BuildRequires:	SFEqt47-gpp-devel
BuildRequires:	SFEdjvulibre-devel

Requires:	SFEgccruntime
Requires:	SFEqt47-gpp
Requires:	SFEdjvulibre


%prep
%setup -q -n %srcname-%version


%build

CPUS=$(psrinfo | awk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads -L%_cxx_libdir"
export LDFLAGS="%_ldflags -pthreads -L%_cxx_libdir -L/usr/gnu/lib -R%_cxx_libdir:/usr/gnu/lib"
export QMAKE=/usr/g++/bin/qmake
export QMAKESPEC=solaris-g++
export QTDIR=/usr/g++
export PKG_CONFIG_PATH="%_cxx_libdir/pkgconfig"

./configure --prefix=%_prefix
#  --with-qt4-dir=/usr/stdcxx --with-qt4-libraries=%_cxx_libdir

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT%_libdir
mv netscape firefox

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/djview
%_bindir/djview4
%dir %attr (-, root, sys) %_datadir
%_datadir/djvu
%_mandir
%_libdir/firefox/plugins


%changelog
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jun 12 2011 - Alex Viskovatoff
- Qt gcc libs are now in their own place
* Tue Apr 12 2011 - Alex Viskovatoff
- Update to 4.7
* Tue Feb  8 2011 - Alex Viskovatoff
- Adapt to Qt gcc libs now being in /usr/stdcxx
* Mon Jan 31 2011 - Alex Viskovatoff
- Initial spec
