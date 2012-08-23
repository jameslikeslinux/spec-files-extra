# 
# spec file for package libreoffice 
# 
# by Ken Mays
#
# LibreOffice is the free power-packed Open Source cross-platform personal productivity suite for
# that gives you six feature-rich applications for all your document production and data processing needs: 
# Writer, Calc, Impress, Draw, Math and Base.
#
# Components of LibreOffice 3.3.3.1
#
# libreoffice-artwork-3.3.3.1.tar.bz2 21 MB
# libreoffice-base-3.3.3.1.tar.bz2 2 MB
# libreoffice-bootstrap-3.3.3.1.tar.bz2 2.6 MB
# libreoffice-build-3.3.3.1.tar.gz 14 MB
# libreoffice-calc-3.3.3.1.tar.bz2 9 MB
# libreoffice-components-3.3.3.1.tar.bz2 4.9 MB
# libreoffice-extensions-3.3.3.1.tar.bz2 4 MB
# libreoffice-extras-3.3.3.1.tar.bz2 37 MB
# libreoffice-filters-3.3.3.1.tar.bz2 11 MB
# libreoffice-help-3.3.3.1.tar.bz2 1.8 MB
# libreoffice-impress-3.3.3.1.tar.bz2 2.5 MB
# libreoffice-l10n-3.3.3.1.tar.bz2 77 MB
# libreoffice-libs-core-3.3.3.1.tar.bz2 16 MB
# libreoffice-libs-extern-3.3.3.1.tar.bz2 615 KB
# libreoffice-libs-extern-sys-3.3.3.1.tar.bz2 37 MB
# libreoffice-libs-gui-3.3.3.1.tar.bz2 10 MB
# libreoffice-postprocess-3.3.3.1.tar.bz2 42 KB
# libreoffice-sdk-3.3.3.1.tar.bz2 1.6 MB
# libreoffice-testing-3.3.3.1.tar.bz2 49 MB
# libreoffice-ure-3.3.3.1.tar.bz2 5.9 MB
# libreoffice-writer-3.3.3.1.tar.bz2 6.5 MB
#
# English (USA) Binary Tarball
#
# LibO_3.3.3.1_Solaris_x86_install-en-US.tar.gz
#
# 

#%define src_name libreoffice
#%define src_url http://download.documentfoundation.org/libreoffice/src/
#%define         piece             base 

Name:           SFElibreoffice
Version:        3.3.3.1
Summary:        Full integrated office productivity suite
URL:            http://www.libreoffice.org
#Source:         %{src_url}/%{src_name}-%{piece}-%{version}.tar.bz2
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SFEhunspell
BuildRequires:  library/perl-5/xml-parser
BuildRequires:	SFErasqal
BuildRequires:	SFEgcc
Requires:	SFEgccruntime
Requires:	SFEgit
Requires:       %{name}-root

%description
LibreOffice is the free power-packed Open Source cross-platform personal productivity suite for
that gives you six feature-rich applications for all your document production and data processing needs: 
Writer, Calc, Impress, Draw, Math and Base.

%prep
%setup -q -n 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export JAVA_HOME="/usr/java"
export CC="/usr/gnu/bin/gcc"
export CXX="/usr/gnu/bin/g++"
export CFLAGS="-g -Os -march=pentium4 -pipe -fopenmp -fno-omit-frame-pointer -I/usr/include -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -Xlinker -i"
export LDFLAGS="-L/lib -R/lib -L/usr/lib -R/usr/lib %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path}"
export LD=/usr/ccs/bin/ld

mkdir git
cd git
./git clone git://anongit.freedesktop.org/libreoffice/bootstrap libo
./autogen.sh --with-num-cpus=4 --with-max-jobs=6 --without-junit --disable-epm 

make -j$CPUS
  
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
  
%files
%defattr (-, root, bin)
%_libdir/libreoffice
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_docdir
%_docdir
%_mandir
  
%changelog
* Ken Mays <kmays2000@gmail.com>
- Initial spec 

