#
# spec file for package SFElyx
#
# includes module: lyx
#

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
Version:	2.0.0beta3
Source:		ftp://ftp.lyx.org/pub/lyx/devel/lyx-2.0/beta3/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEgcc
BuildRequires:	SFEqt47-devel
BuildRequires:	SFEboost-stdcxx-devel

Requires:	SFEgccruntime
Requires:	SFEqt47-gpp

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
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS="%_ldflags -L/usr/lib/g++/%_gpp_version -R/usr/lib/g++/%_gpp_version"

./configure --prefix=%_prefix \
  --with-qt4-dir=/usr/stdcxx --with-qt4-libraries=/usr/lib/g++/%_gpp_version

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
* Sun Jan 30 2011 - Alex Viskovatoff
- Initial spec
