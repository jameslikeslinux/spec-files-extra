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
Version:                 0.9.11.3
URL:		         http://libvirt.org
Source:		         http://libvirt.org/sources/libvirt-%{version}.tar.gz
Patch1:                  libvirt-01-virnetdev.diff
Patch2:                  libvirt-02-cfmakeraw.diff
Patch3:                  libvirt-03-noversionscript.diff
Patch4:                  libvirt-04-removexvmctrl.diff
Patch5:                  libvirt-05-nolinuxheaders.diff
Patch6:                  libvirt-06-name_max.diff
Patch7:                  libvirt-07-sys_mntent.diff
Patch8:                  libvirt-08-linux_capabilities.diff
Patch9:                  libvirt-09-cmsg.diff
Patch10:                 libvirt-10-io_macro.diff
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
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -D_XPG4_2"
#export LDFLAGS="%_ldflags"
./configure --prefix=/usr			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --with-qemu

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/etc/logrotate.d
rm -rf $RPM_BUILD_ROOT/etc/sysctl.d
rm $RPM_BUILD_ROOT/usr/lib/charset.alias

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libvirt*
%dir %attr (0755, root, bin) %{_libdir}/python2.6
%{_libdir}/python2.6/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/libvirt
%{_includedir}/libvirt/*
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/locale/af
%dir %attr (0755, root, other) %{_datadir}/locale/af/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/am
%dir %attr (0755, root, other) %{_datadir}/locale/am/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ar
%dir %attr (0755, root, other) %{_datadir}/locale/ar/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/as
%dir %attr (0755, root, other) %{_datadir}/locale/as/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/be
%dir %attr (0755, root, other) %{_datadir}/locale/be/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/bg
%dir %attr (0755, root, other) %{_datadir}/locale/bg/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/bn
%dir %attr (0755, root, other) %{_datadir}/locale/bn/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/bn_IN
%dir %attr (0755, root, other) %{_datadir}/locale/bn_IN/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/bs
%dir %attr (0755, root, other) %{_datadir}/locale/bs/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ca
%dir %attr (0755, root, other) %{_datadir}/locale/ca/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/cs
%dir %attr (0755, root, other) %{_datadir}/locale/cs/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/cy
%dir %attr (0755, root, other) %{_datadir}/locale/cy/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/da
%dir %attr (0755, root, other) %{_datadir}/locale/da/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/de
%dir %attr (0755, root, other) %{_datadir}/locale/de/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/el
%dir %attr (0755, root, other) %{_datadir}/locale/el/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/en_GB
%dir %attr (0755, root, other) %{_datadir}/locale/en_GB/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/es
%dir %attr (0755, root, other) %{_datadir}/locale/es/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/et
%dir %attr (0755, root, other) %{_datadir}/locale/et/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/eu_ES
%dir %attr (0755, root, other) %{_datadir}/locale/eu_ES/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/fa
%dir %attr (0755, root, other) %{_datadir}/locale/fa/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/fi
%dir %attr (0755, root, other) %{_datadir}/locale/fi/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/fr
%dir %attr (0755, root, other) %{_datadir}/locale/fr/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/gl
%dir %attr (0755, root, other) %{_datadir}/locale/gl/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/gu
%dir %attr (0755, root, other) %{_datadir}/locale/gu/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/he
%dir %attr (0755, root, other) %{_datadir}/locale/he/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/hi
%dir %attr (0755, root, other) %{_datadir}/locale/hi/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/hr
%dir %attr (0755, root, other) %{_datadir}/locale/hr/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/hu
%dir %attr (0755, root, other) %{_datadir}/locale/hu/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/hy
%dir %attr (0755, root, other) %{_datadir}/locale/hy/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/id
%dir %attr (0755, root, other) %{_datadir}/locale/id/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/is
%dir %attr (0755, root, other) %{_datadir}/locale/is/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/it
%dir %attr (0755, root, other) %{_datadir}/locale/it/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ja
%dir %attr (0755, root, other) %{_datadir}/locale/ja/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ka
%dir %attr (0755, root, other) %{_datadir}/locale/ka/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/kn
%dir %attr (0755, root, other) %{_datadir}/locale/kn/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ko
%dir %attr (0755, root, other) %{_datadir}/locale/ko/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ku
%dir %attr (0755, root, other) %{_datadir}/locale/ku/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/lo
%dir %attr (0755, root, other) %{_datadir}/locale/lo/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/lt
%dir %attr (0755, root, other) %{_datadir}/locale/lt/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/lv
%dir %attr (0755, root, other) %{_datadir}/locale/lv/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/mk
%dir %attr (0755, root, other) %{_datadir}/locale/mk/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ml
%dir %attr (0755, root, other) %{_datadir}/locale/ml/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/mr
%dir %attr (0755, root, other) %{_datadir}/locale/mr/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ms
%dir %attr (0755, root, other) %{_datadir}/locale/ms/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/my
%dir %attr (0755, root, other) %{_datadir}/locale/my/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/nb
%dir %attr (0755, root, other) %{_datadir}/locale/nb/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/nl
%dir %attr (0755, root, other) %{_datadir}/locale/nl/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/nn
%dir %attr (0755, root, other) %{_datadir}/locale/nn/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/nso
%dir %attr (0755, root, other) %{_datadir}/locale/nso/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/or
%dir %attr (0755, root, other) %{_datadir}/locale/or/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/pa
%dir %attr (0755, root, other) %{_datadir}/locale/pa/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/pl
%dir %attr (0755, root, other) %{_datadir}/locale/pl/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/pt
%dir %attr (0755, root, other) %{_datadir}/locale/pt/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/pt_BR
%dir %attr (0755, root, other) %{_datadir}/locale/pt_BR/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ro
%dir %attr (0755, root, other) %{_datadir}/locale/ro/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ru
%dir %attr (0755, root, other) %{_datadir}/locale/ru/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/si
%dir %attr (0755, root, other) %{_datadir}/locale/si/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/sk
%dir %attr (0755, root, other) %{_datadir}/locale/sk/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/sl
%dir %attr (0755, root, other) %{_datadir}/locale/sl/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/sq
%dir %attr (0755, root, other) %{_datadir}/locale/sq/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/sr
%dir %attr (0755, root, other) %{_datadir}/locale/sr/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/sr@latin
%dir %attr (0755, root, other) %{_datadir}/locale/sr@latin/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/sv
%dir %attr (0755, root, other) %{_datadir}/locale/sv/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ta
%dir %attr (0755, root, other) %{_datadir}/locale/ta/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/te
%dir %attr (0755, root, other) %{_datadir}/locale/te/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/th
%dir %attr (0755, root, other) %{_datadir}/locale/th/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/tr
%dir %attr (0755, root, other) %{_datadir}/locale/tr/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/uk
%dir %attr (0755, root, other) %{_datadir}/locale/uk/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/ur
%dir %attr (0755, root, other) %{_datadir}/locale/ur/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/vi
%dir %attr (0755, root, other) %{_datadir}/locale/vi/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/vi_VN
%dir %attr (0755, root, other) %{_datadir}/locale/vi_VN/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/zh_CN
%dir %attr (0755, root, other) %{_datadir}/locale/zh_CN/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/zh_TW
%dir %attr (0755, root, other) %{_datadir}/locale/zh_TW/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/zu
%dir %attr (0755, root, other) %{_datadir}/locale/zu/LC_MESSAGES
%{_datadir}/locale/*/LC_MESSAGES/libvirt.mo
%dir %attr (0755, root, other) %{_datadir}/doc/libvirt-%{version}
%{_datadir}/doc/libvirt-%{version}/*
%dir %attr (0755, root, other) %{_datadir}/doc/libvirt-python-%{version}
%{_datadir}/doc/libvirt-python-%{version}/*
%dir %attr (0755, root, other) %{_datadir}/augeas
%{_datadir}/augeas/*
%dir %attr (0755, root, other) %{_datadir}/libvirt
%{_datadir}/libvirt/*
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%dir %attr (0755, root, other) %{_datadir}/gtk-doc/html/libvirt
%{_datadir}/gtk-doc/html/libvirt/*
%dir %attr (0755, root, sys) /etc
%dir %attr (0755, root, other) /etc/libvirt
/etc/libvirt/*
%dir %attr (0755, root, bin) /etc/sasl2
/etc/sasl2/*
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) /var/log
%dir %attr (0755, root, other) /var/log/libvirt
/var/log/libvirt/*
%dir %attr (0755, root, sys) /var/run
%dir %attr (0755, root, other) /var/run/libvirt
/var/run/libvirt/*
%dir %attr (0755, root, other) /var/lib/libvirt
/var/lib/libvirt/*
%dir %attr (0755, root, bin) /var/cache
%dir %attr (0755, root, other) /var/cache/libvirt
%dir %attr (0755, root, other) /var/cache/libvirt/qemu

%changelog
* Sun Apr 29 2012 - Logan Bruns <logan@gedanken.org>
- Porting changes to support qemu/kvm.
* Thu Mar 15 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
