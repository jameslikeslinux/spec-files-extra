#
# spec file for package SFExcircuit
#
# includes module(s): xcircuits
#
%include Solaris.inc

Name:                    SFExcircuit
Summary:                 Electrical circuit schematic diagram drawing program
Group:                   Applications/Graphics and Imaging
Version:                 3.7.26
Group:                   Utility
Source:                  http://opencircuitdesign.com/xcircuit/archive/xcircuit-%{version}.tgz
License:		 GPLv2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          xcircuit.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWxwrtl
Requires: SUNWzlib
Requires: SUNWlibms

%prep
%setup -q -n xcircuit-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags"
./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}                 \
	    --mandir=%{_mandir}			\
	    --without-tcl
	    
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/xcircuit-*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Mon Jul 25 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Thu Jun 16 2011 - N.B.Prashanth<nbprash.mit@gmail.com>
- Bump to 3.7.26
* Sun Jul 23 2006 - laca@sun.com
- rename to SFExcircuit
- delete -share subpkg
- update file attributes
* Thu Apr 27 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Bump up version from 3.4.10 to 3.4.21
* Mon Nov 24,2005 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec

