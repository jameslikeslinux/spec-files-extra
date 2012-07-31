#
# spec file for package SFEfreeimage.spec
#
# includes module(s): freeimage
#
%include Solaris.inc

%define src_name	FreeImage
%define src_vermaj	3
%define src_vermin	15
%define src_vermic	2
%define src_version	%{src_vermaj}%{src_vermin}%{src_vermic}

Name:		SFEfreeimage
IPS_Package_Name:	image/library/freeimage
Summary:	free image library
Version:	%{src_vermaj}.%{src_vermin}.%{src_vermic}
Source:		%{sf_download}/freeimage/%{src_name}%{src_version}.zip
URL:		http://freeimage.sourceforge.net
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}
find . -type f -exec dos2unix {} {} \;

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make -f Makefile.solaris

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_includedir}
install -m 644 Source/FreeImage.h %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_libdir}
install -m 755 libfreeimage-%{version}.so %{buildroot}/%{_libdir}
cd %{buildroot}/%{_libdir} && ln -s libfreeimage-%{version}.so libfreeimage.so.%{src_vermaj}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sun Mar 11 2012 - Milan Jurik
- bump to 3.15.2
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
