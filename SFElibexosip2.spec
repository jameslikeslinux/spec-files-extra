#
# spec file for package SFElibexosip2
#
# includes module(s): libexosip2
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:		SFElibexosip2
Summary:	eXosip is a library that hides the complexity of using the SIP protocol for mutlimedia session establishement
Version:	3.5.0
Source:		http://download.savannah.gnu.org/releases/exosip/libeXosip2-%{version}.tar.gz
URL:		http://savannah.nongnu.org/projects/exosip/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWaudh
BuildRequires: SUNWgnome-common-devel
Requires: SFElibosip2
BuildRequires: SFElibosip2-devel

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libeXosip2-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags} -lnsl"

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
%{_bindir}
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Thu Feb 10 2011 - Milan Jurik
- initial spec
