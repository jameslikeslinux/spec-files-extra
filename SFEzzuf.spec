#
# spec file for package SFEzzuf
#
# includes module(s): zzuf
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname zzuf

Name:                    SFEzzuf
IPS_Package_Name:	 sfe/developer/zzuf
Summary:                 zzuf - multi-purpose fuzzer
Group:                   Utility
Version:                 0.13
URL:		         http://caca.zoy.org/wiki/zzuf
Source:		         http://caca.zoy.org/files/zzuf/zzuf-%{version}.tar.gz
Patch1:                  zzuf-01-void_rewind.diff
Patch2:                  zzuf-02-void_socklen_t.diff
License: 		 Public Domain (See copyright)
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
zzuf is a transparent application input fuzzer. Its purpose is to find
bugs in applications by corrupting their user-contributed data (which
more than often comes from untrusted sources on the Internet). It
works by intercepting file and network operations and changing random
bits in the program’s input. zzuf’s behaviour is deterministic, making
it easier to reproduce bugs. Its main areas of use are:

    quality assurance: use zzuf to test existing software, or
                       integrate it into your own software’s testsuite

    security: very often, segmentation faults or memory corruption
              issues mean a potential security hole, zzuf helps
              exposing some of them

    code coverage analysis: use zzuf to maximise code coverage 

zzuf’s primary target is media players, image viewers and web
browsers, because the data they process is inherently insecure, but it
was also successfully used to find bugs in system utilities such as
objdump.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -lnsl -lsocket"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/zzuf
%{_libdir}/zzuf/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Wed May 23 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
