#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define	src_name	silgraphite

Name:		SFEsilgraphite
IPS_Package_Name:	system/library/silgraphite
Summary:	smart font system consists of an engine
Group:		System/Libraries
Version:	2.3.1
Source:		%{sf_download}/%{src_name}/%{version}/%{src_name}-%{version}.tar.gz
Patch1:		silgraphite-01-sunstudio.diff
URL:		http://silgraphite.sourceforge.net/
License:	LGPLv2.1+
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%name

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

sh ./configure --prefix=%{_prefix}	\
	--enable-static=no	\
	--enable-shared=yes

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/lib*.la

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}/*.so*
%{_libdir}/pango

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Nov 07 2011 - Milan Jurik
- initial spec
