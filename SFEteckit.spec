#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define	src_version	2_5_1
%define	src_name	TECkit

Name:		SFEteckit
IPS_Package_Name:	system/library/teckit
Summary:	low-level toolkit for encoding conversions
Group:		System/Libraries
Version:	2.5.1
Source:		http://scripts.sil.org/svn-view/teckit/TAGS/%{src_name}_%{src_version}.tar.gz
URL:		http://scripts.sil.org/TECkit
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
%setup -q -n %{src_name}_%{src_version}

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
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Mon Oct 31 2011 - Milan Jurik
- Initial spec
