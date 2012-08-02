#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

Name:	SFEopenoffice-dmake
IPS_Package_Name:	openoffice/dmake
Version:	4.12.1
Summary:	dmake for OpenOffice build
License:	GPLv2+ or Artistic
URL:		https://code.google.com/a/apache-extras.org/p/dmake/
Source:		http://dmake.apache-extras.org.codespot.com/files/dmake-%{version}.tar.bz2
Group:		Development/Distribution Tools
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Dmake is a make utility similar to GNU make or the Workshop dmake. This utility has an irregular syntax but is available for FreeBSD, Linux, Solaris, Win32 and other platforms. It is used by the OpenOffice.org build system, although for some time now Apache OpenOffice.Org and it's derivatives have been considering replacing it definitely with a GNUmake-only build system.

This version of dmake is a modified version of Dennis Vadura's GPL'ed dmake. The original sources were available on WTIcorp.com. As this site has not been reachable for some time the SUN OpenOffice.org team adopted this utility and continued its development in OOo's Version Control System. 

%prep
%setup -q -n dmake-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix}/openoffice	\
	--enable-spawn

make -j$CPUS


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_prefix}/openoffice/bin
%dir %attr (0755, root, sys) %{_prefix}/openoffice/share
%{_prefix}/openoffice/share/*

%changelog
* Sun Jan 08 2012 - Milan Jurik
- initial spec
