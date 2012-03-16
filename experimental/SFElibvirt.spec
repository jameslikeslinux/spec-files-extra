#
# spec file for package SFElibvirt
#
# includes module(s): libvirt
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define _basedir /
%define _bindir /usr/bin
%define _sbindir /usr/sbin
%define _mandir /usr/share/man
%define _includedir /usr/include
%define _libdir /usr/lib
%define _libexecdir /usr/lib
%define _datadir /usr/share

%define srcname libvirt

Name:                    SFElibvirt
IPS_Package_Name:	 sfe/system/library/libvirt
Summary:                 libvirt - The virtualization API
Group:                   Utility
Version:                 0.9.10
URL:		         http://libvirt.org
Source:		         http://libvirt.org/sources/libvirt-%{version}.tar.gz
Patch1:                  libvirt-01-virnetdev.diff
Patch2:                  libvirt-02-cfmakeraw.diff
Patch3:                  libvirt-03-noversionscript.diff
Patch4:                  libvirt-04-removexvmctrl.diff
License: 		 LGPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Libvirt is collection of software that provides a convenient way to
manage virtual machines and other virtualization functionality, such
as storage and network interface management. These software pieces
include an API library, a daemon (libvirtd), and a command line
utility (virsh).

An primary goal of libvirt is to provide a single way to manage
multiple different virtualization providers/hypervisors. For example,
the command 'virsh list --all' can be used to list the existing
virtual machines for any supported hypervisor (KVM, Xen, VMWare ESX,
etc.) No need to learn the hypervisor specific tools!

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=/usr			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/etc/logrotate.d
rm -rf $RPM_BUILD_ROOT/etc/sysctl.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%dir %attr (0755, root, bin) %{_includedir}/libvirt
%{_includedir}/libvirt/*
%{_datadir}/locale/*/LC_MESSAGES/libvirt.mo
%dir %attr (0755, root, bin) %{_datadir}/doc/libvirt-%{version}
%{_datadir}/doc/libvirt-%{version}/*
%dir %attr (0755, root, bin) %{_datadir}/doc/libvirt-python-%{version}
%{_datadir}/doc/libvirt-python-%{version}/*
%dir %attr (0755, root, bin) %{_datadir}/augeas
%{_datadir}/augeas/*
%dir %attr (0755, root, bin) %{_datadir}/libvirt
%{_datadir}/libvirt/*
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html/libvirt
%{_datadir}/gtk-doc/html/libvirt/*
%dir %attr (0755, root, bin) /etc/libvirt
/etc/libvirt/*
%dir %attr (0755, root, bin) /etc/sasl2
/etc/sasl2/*
%dir %attr (0755, root, bin) /var/log/libvirt
/var/log/libvirt/*
%dir %attr (0755, root, bin) /var/run/libvirt
/var/run/libvirt/*
%dir %attr (0755, root, bin) /var/lib/libvirt
/var/lib/libvirt/*
%dir %attr (0755, root, bin) /var/cache/libvirt

%changelog
* Thu Mar 15 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
