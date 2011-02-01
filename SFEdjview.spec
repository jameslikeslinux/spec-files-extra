#
# spec file for package SFEdjview
#
# includes module: djview
#

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define srcname djview4

Name:		SFEdjview
Summary:	DjVu file viewer
URL:		http://djvu.sourceforge
Vendor:		Léon Bottou
License:	GPL
Version:	4.6
Source:		%sf_download/project/djvu/DjView/4.6/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEgcc
BuildRequires:	SFEqt47-devel
BuildRequires:	SFEdjvulibre-devel

Requires:	SFEgccruntime
Requires:	SFEqt47-gpp
Requires:	SFEdjvulibre


%prep
%setup -q -n %srcname-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS="%_ldflags -L/usr/lib/g++/%_gpp_version -R/usr/lib/g++/%_gpp_version"
export QMAKE=/usr/stdcxx/bin/qmake
export QMAKESPEC=solaris-g++
export QTDIR=/usr/stdcxx

./configure --prefix=%_prefix \
  --with-qt4-dir=/usr/stdcxx --with-qt4-libraries=/usr/lib/g++/%_gpp_version

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
* Mon Jan 31 2011 - Alex Viskovatoff
- Initial spec
