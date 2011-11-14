#
# Initial spec file for package SFExen 
# By Ken Mays
#
# Note: GCC >=3.4.3, GCC 4.6.1 tested


%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:		SFExen
Summary:	xen - a virtual machine monitor for x86 (Xen Hypervisor) 
URL:		http://www.xen.org
Version:	4.1.1
Group:		System/Kernel
License:	GPLv2+
Source:         http://bits.xensource.com/oss-xen/release/4.1.1/xen-4.1.1.tar.gz

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc
Requires: SUNWpostrun-root

%description
Xen is a virtual machine monitor for x86 that supports execution of
multiple guest operating systems with unprecedented levels of
performance and resource isolation.

%prep
%setup -q -n xen-%version
#%patch1 -p1

%build
export CC=gcc
export CXX=g++
#export LDFLAGS="%_ldflags"

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

make world -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/xen/*


%changelog
* Thu Oct 6 2011 - Ken Mays <kmays2000@gmail.com>
- Research xc_solaris.c issue
- Initial spec (xen 4.1.1)
