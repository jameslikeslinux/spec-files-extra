#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:		SFEt1lib
IPS_Package_Name:	system/library/t1lib
Summary:        Library allowing a programmer to generate/rasterize bitmaps from Adobe (TM) Type 1 fonts
Group:		System/Multimedia Libraries
Version:	5.1.2
Source:		ftp://sunsite.unc.edu/pub/Linux/libs/graphics/t1lib-%{version}.tar.gz
URL:		http://www.t1lib.org/
License:	GPLv2+
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n t1lib-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}	\
	--disable-static	\
	--enable-shared

make -j$CPUS without_doc

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/libt1.la
rm -f %{buildroot}%{_libdir}/libt1x.la

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/t1lib

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Mon Oct 24 2011 - Milan Jurik
- Initial spec
