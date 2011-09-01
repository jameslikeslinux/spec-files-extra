#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_version 0.2.13-3

Name:                SFEmpg321
Summary:             A fully free clone of mpg123, a command-line mp3 player
Version:             0.2.13.3
Source:              %{sf_download}/mpg321/mpg321-%{src_version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElibao-devel
Requires: SFElibao
BuildRequires: SFElibmad-devel
Requires: SFElibmad

%prep
%setup -q -n mpg321

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --enable-ipv6        \
            --disable-mpg123-symlink

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Thu Sep 01 2011 - Milan Jurik
- bump to 0.2.13-3 
* Mon Sep 25 2006 - Eric Boutilier
- Initial spec
