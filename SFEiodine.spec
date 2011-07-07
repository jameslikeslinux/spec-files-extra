#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_version 0.6.0-rc1

Name:                SFEiodine
Summary:             iodine - IP over DNS is now easy
Version:             0.5.99.1
URL:                 http://code.kryo.se/iodine/
Source:              http://code.kryo.se/iodine/iodine-%{src_version}.tar.gz
Patch1:              iodine-01-solaris.diff
Patch2:              iodine-02-nogcc.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWzlib
Requires: SFEtun

%description
iodine is a piece of software that lets you tunnel IPv4 data through a DNS
server. This can be usable in different situations where internet access is
firewalled, but DNS queries are allowed.

%prep
%setup -q -n iodine-%{src_version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT" prefix="/usr"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%changelog
* Fri Mar 25 2011 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.6.0-rc1
- Add patch1, patch2
* Tue Sep 15 2009 - trisk@acm.jhu.edu
- Bump to 0.5.2
* Fri May 23 2008 - trisk@acm.jhu.edu
- Bump to 0.4.1
* Wed Nov 28 2007 - trisk@acm.jhu.edu
- Initial spec
