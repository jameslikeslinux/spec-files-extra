#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define	src_name	lft

Name:		SFElft
IPS_Package_Name:	diagnostic/lft
Summary:	smart font system consists of an engine
Group:		Diagnostic
Version:	3.33
#REAL location: Source:		http://pwhois.org/dl/index.who?file=lft-%{version}.tar.gz
Source:		http://fossies.org/unix/privat/%{src_name}-%{version}.tar.gz
URL:		http://pwhois.org/lft
License:	Open Source
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:  system/library/libpcap
Requires:	system/library/libpcap

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# Use gcc...
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} 

make -j$CPUS

%install
sudo rm -rf %{buildroot}
sudo make install DESTDIR=%{buildroot}

%clean
sudo rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%{_mandir}

%changelog
* Fri Nov 18 2011 - Predrag Zecevic
- initial spec
