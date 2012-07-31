#
# spec file for package pythia8
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:         pythia8
License:      GPL
Group:        Math
Version:      8.1.57
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      An event generator for a large number of physics processes

%define fileversion %(echo %{version} | tr -d .)
%define majorversion %(echo %{version} | cut -d "." -f1-2)
Source:       http://home.thep.lu.se/~torbjorn/pythia8/pythia%{fileversion}.tgz
URL:          http://home.thep.lu.se/~torbjorn/Pythia.html
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n pythia%fileversion


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

/usr/bin/bash ./configure --enable-shared
#            --enable-shared		\
#            --enable-64bits		\
#            --enable-gzip  # This is experimental

gmake -j$CPUS 


%install
install -d -m 0755 $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 lib/liblhapdfdummy.so lib/libpythia8.so \
        $RPM_BUILD_ROOT/%{_libdir}
install -d -m 0755 $RPM_BUILD_ROOT/%{_includedir}/pythia-%{majorversion}
install -m 0755 include/*.h $RPM_BUILD_ROOT/%{_includedir}/pythia-%{majorversion}
install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}/pythia-%{majorversion}/htmldoc
install -m 0755 htmldoc/* $RPM_BUILD_ROOT/%{_docdir}/pythia-%{majorversion}/htmldoc
# Why is this directory empty?
#rm -r phpdoc/files
mv phpdoc/files phpdocfiles
install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}/pythia-%{majorversion}/phpdoc
install -m 0755 phpdoc/* $RPM_BUILD_ROOT/%{_docdir}/pythia-%{majorversion}/phpdoc
install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}/pythia-%{majorversion}/xmldoc
install -m 0755 xmldoc/* $RPM_BUILD_ROOT/%{_docdir}/pythia-%{majorversion}/xmldoc


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Jan 13 2012 - James Choi
- Initial spec
