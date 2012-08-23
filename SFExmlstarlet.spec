#
# spec file for package SFExmlstarlet
#
# includes module(s): xmlstarlet
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name xmlstarlet

Name:                    SFExmlstarlet
IPS_Package_Name:	 text/xmlstarlet
Summary:                 XMLStarlet - Command Line Toolkit to query/edit/check/transform XML documents
Group:                   Utility
Version:                 1.3.1
URL:		         http://xmlstar.sourceforge.net
Source:		         %{sf_download}/project/xmlstar/%{src_name}/%{version}/%{src_name}-%{version}.tar.gz 
License: 		 MIT
Patch1:                  xmlstarlet-01-configure.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlxsl
Requires: SUNWlxml

%description
XMLStarlet is a set of command line utilities (tools) which can be
used to transform, query, validate, and edit XML documents and files
using simple set of shell commands in similar way it is done for plain
text files using UNIX grep, sed, awk, diff, patch, join, etc commands.

%prep
rm -rf %name-%version
%setup -q -n xmlstarlet-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --with-libxml-include-prefix=%{_prefix}/include/libxml2 \
            --program-transform-name=s/xml/xmlstarlet/

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
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sun Feb 19 2012- logan@gedanken.org
- Initial spec.
