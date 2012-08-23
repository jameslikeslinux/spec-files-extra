#
# spec file for package SFElibosip2
#
# includes module(s): libosip2
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:		SFElibosip2
IPS_Package_Name:	library/libosip2
Summary:	oSIP is an implementation of SIP
Version:	3.6.0
Group:		System/Libraries
Source:		http://ftp.gnu.org/gnu/osip/libosip2-%{version}.tar.gz
URL:		http://www.gnu.org/software/osip/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n libosip2-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

./configure --prefix=%{_prefix} --disable-static

make -j$CPUS

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*pc
%{_includedir}

%changelog
* Wed Feb 08 2012 - Milan Jurik
- bump to 3.6.0
* Thu Feb 10 2011 - Milan Jurik
- initial spec
