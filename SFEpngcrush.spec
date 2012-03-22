#
# spec file for package SFEpngcrush
#
# includes module(s): pngcrush
#
%include Solaris.inc

%define src_name	pngcrush

Name:		SFEpngcrush
IPS_Package_Name:	image/pngcrush
Summary:	Utility for recompressing PNG files
Version:	1.7.25
Group:		Applications/Graphics and Imaging
License:	pngcrush
Source:		 %{sf_download}/project/pmt/pngcrush/%{version}/%{src_name}-%{version}.tar.bz2
URL:		http://pmt.sourceforge.net/pngcrush/
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright:	%{name}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms
Requires: SUNWzlib

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
make -j$CPUS CC="$CC" LD="$CC" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 pngcrush $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/pngcrush

%changelog
* Wed Mar 21 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.25
* Sun Dec 11 2011 - Milan Jurik
- bump to 1.7.22
* Thu Aug 14 2008 - laca@sun.com
- create
