#
# spec file for package telepathy-gabble
#
# Owner:elaine_sun
#

Name:           telepathy-gabble
License:        GPL
Group:          Applications/Internet
Version:        0.10.3
Release:        1
Distribution:   Java Desktop System
Vendor:         Oracle, Inc.
Summary:        A Jabber/XMPP connection manager
Source:	        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
URL:            http://telepathy.freedesktop.org/wiki
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/telepathy-gabble
# date:2010-10-12 owner:jefftsai type:bug
Patch1:         telepathy-gabble-01-compatible.diff
# jingleinfo security bug
Patch10:	telepathy-gabble-10-jingleinfo.diff

Autoreqprov: on
Prereq:      /sbin/ldconfig

%description
Gabber is a Jabber/XMPP connection manager for the Telepathy framework, 
currently supporting: single-user chats, multi-user chats, voice/video
calling and file transfer with Jabber/XMPP and Google Talk interoperability.
%prep
%setup -q
%patch1 -p1
%patch10 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%{optflags} -I/usr/gnu/include -DBSD_COMP"
export CXXFLAGS="%{cxx_optflags} -I/usr/gnu/include"
export LDFLAGS="%{_ldflags} %{gnu_lib_path} -lsocket -lresolv -lnsl"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
  export CFLAGS="-m64 $CFLAGS"
  export CXXFLAGS="-m64 $CXXFLAGS"
  export LDFLAGS="-m64 $LDFLAGS"
fi



./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*
%{_datadir}/doc/*

%changelog
* Sat Feb 19 2011 - Milan Jurik
- fix jingleinfo security bug
* Sun Feb 13 2011 - Milan Jurik
- disable multiarch build
* Fri Oct 08 2010 - jeff.cai@oracle.com
- created, version 0.10.3
