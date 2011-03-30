#
# spec file for package SFElyx
#
# includes module: lyx
#

# To be able to typeset LyX documents, you need to have TeX installed.
# Since SFEtexlive.spec is not currently maintained, it is probably best
# to install TeX Live using its own native installer.  See
#   http://www.tug.org/texlive/acquire-netinstall.html.
# You need to make sure that the various TeX executables are in your PATH.
# The TeX Live installer gives you the option of creatingg symbolic links
# to them automatically; creating symbolic links of TeX executables to
# a directory in your PATH is probably the best way of making LyX find them.

# Since the libraries of SFEqt47-gpp are now in a non-standard location,
# you will need to do, for example:
# pfexec elfedit -e 'dyn:runpath /usr/gnu/lib' pdftex

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define srcname lyx

Name:		SFElyx
Summary:	Graphical LaTeX front end: What You See Is What You Mean
URL:		http://www.lyx.org
Vendor:		LyX Team
License:	GPL
#Version:	1.6.8
#Source:	ftp://ftp.lyx.org/pub/lyx/stable/1.6.x/%srcname-%version.tar.bz2
Version:	2.0.0rc2
Source:		ftp://ftp.lyx.org/pub/lyx/devel/%srcname-2.0/rc2/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEgcc
BuildRequires:	SFEqt47-gpp-devel

Requires:	SFEgccruntime
Requires:	SFEqt47-gpp
Requires:	SFElibiconv

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# The LyX code is really nasty to Sun Studio
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads -I/usr/g++/include -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS="%_ldflags -pthreads -L/usr/g++/lib -R/usr/g++/lib"

# SFEhunspell is built with CC, so SFElyx can't link against it
./configure --prefix=%_prefix --with-qt4-dir=/usr/g++ --without-hunspell

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/lyx
%_bindir/lyxclient
%_bindir/tex2lyx
%dir %attr (-, root, sys) %_datadir
%_datadir/%srcname
%_mandir

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif


%changelog
* Wed Mar 30 2011 - Alex Viskovatoff
- Adapt to gcc-built Qt now being in /usr/g++
- Update to 2.0.0rc2; disable hunspell; remove build dependency on Boost
* Tue Feb  8 2011 - Alex Viskovatoff
- Adapt to Qt gcc libs now being in /usr/stdcxx
* Sun Jan 30 2011 - Alex Viskovatoff
- Initial spec
