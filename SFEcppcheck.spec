#
# spec file for package SFEcppcheck
#
# includes module(s): cppcheck
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname cppcheck

Name:                    SFEcppcheck
IPS_Package_Name:	 sfe/developer/cppcheck
Summary:                 Cppcheck - A tool for static C/C++ code analysis
Group:                   Utility
Version:                 1.54
URL:		         http://cppcheck.sourceforge.net
Source:		         %{sf_download}/project/%{srcname}/%{srcname}/%{version}/%{srcname}-%{version}.tar.bz2
Patch1:                  cppcheck-01-strings.diff
Patch2:                  cppcheck-02-fmod.diff
Patch3:                  cppcheck-03-count.diff
Patch4:                  cppcheck-04-string.diff
Patch5:                  cppcheck-05-const-mismatch.diff
Patch6:                  cppcheck-06-docbook.diff
License: 		 GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: data/docbook
Requires: library/pcre

%description
Cppcheck is an static analysis tool for C/C++ code. Unlike C/C++
compilers and many other analysis tools it does not detect syntax
errors in the code. Cppcheck primarily detects the types of bugs that
the compilers normally do not detect. The goal is to detect only real
errors in the code (i.e. have zero false positives).

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -library=stlport4 -staticlib=stlport4"
export LDFLAGS="%_ldflags"

make -j$CPUS all man HAVE_RULES=yes

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp cppcheck.1 $RPM_BUILD_ROOT/%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sat May 19 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
