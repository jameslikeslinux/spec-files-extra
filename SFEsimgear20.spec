#
# spec file for package SFESimGear.spec
# Gilles Dauphin
#
# includes module(s): SimGear
#
%include Solaris.inc

%define cc_is_gcc 1
%define _gpp /usr/bin/g++
%include base.inc

%define src_name	simgear
%define src_url		http://mirrors.ibiblio.org/pub/mirrors/simgear/ftp/Source 

Name:                   SFESimGear20
Summary:                Simulator Construction Tools
Version:                2.4.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
Group:			Applications/Games
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SFEopenal-devel
Requires:		SFEopenal
BuildRequires:		SFEfreealut-devel
Requires:		SFEfreealut
Requires:		SFEplib-gpp
# <km> Note: Use OpenSceneGraph 3.0.1  
Requires:		SFEosg

%prep
%setup -q -c -n  %{name}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}
export CC=/usr/bin/cc
export CXX=/usr/bin/g++
export CFLAGS="-I%{_prefix}/X11/include -I%{_includedir}"
export CXXFLAGS="-I%{_prefix}/X11/include -I%{_includedir}"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
#/bin/bash ./autogen.sh --prefix=%{_prefix}
/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix} \
	--with-osg=%{_prefix} \
	--with-boost=%{_prefix} \
	--with-boost-libdir=%{_libdir}

make  -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
# TODO: make shared libs
#rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}
%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.a*

%changelog
* Fri 02 Sept 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2.4.0 
- Built with oi_151 & GCC 4.6.1
* May 2010 - Gilles Dauphin
- Initial version for 2.0
