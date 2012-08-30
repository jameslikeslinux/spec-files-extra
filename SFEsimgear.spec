#
# spec file for package SFESimGear.spec
# Gilles Dauphin
#
# includes module(s): SimGear
#
%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	simgear
%define src_url		ftp://ftp.de.simgear.org/pub/simgear/Source

Name:		SFEsimgear
IPS_Package_Name:	library/simgear
Summary:	Simulator Construction Tools
Version:	2.8.0
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		simgear-01-stdlib.diff
Patch2:		simgear-02-isnan.diff
Group:		System/Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SFEopenal-devel
Requires:	SFEopenal
BuildRequires:	SFEfreealut-devel
Requires:	SFEfreealut
BuildRequires:	SFEplib-gpp-devel
Requires:	SFEplib-gpp
BuildRequires:	SFEosg-devel
Requires:	SFEosg
BuildRequires:	SFEboost-gpp-devel
Requires:	SFEboost-gpp

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags} -I%{_includedir}"
export CXXFLAGS="%{cxx_optflags} -I%{_includedir}"
export LDFLAGS="%{_ldflags} -lsocket -lnsl -L%{_libdir} -R%{_libdir}"

mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ..

make -j$CPUS 

%install
rm -rf %{buildroot}
cd build && make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_libdir}/lib*.a

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Thu Aug 30 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 2.8.0
* Sat Jun 23 2012 - Thomas Wagner
- rename package name to lower case
* Sun Mar 04 2012 - Milan Jurik
- merge from SFEsimgear20, bump to 2.6.0
* May 2010 - Gilles Dauphin
- back to 1.0 will create a 2.0 spec file (Milan feedback)
* Mar 2010 - Gilles dauphin
- search includedir event if it is in /usr/SFE (exemple)
* Mon Nov 17 2008 - dauphin@enst.fr
- Initial version
