
# spec file for package SFEspidermonkey
#
# includes module(s): spidermonkey
#
%define cc_is_gcc 1
%include Solaris.inc

Name:                    SFEspidermonkey
IPS_Package_Name:	runtime/javascript/spidermonkey
Summary:                 Mozilla SpiderMonkey JavaScript Engine.
Version:                 1.8.5
Source:                  http://ftp.mozilla.org/pub/mozilla.org/js/js185-1.0.0.tar.gz
# Note these patches are copied from spec-files, the latest patches for Firefox
# version 4.
Patch1:                  spidermonkey-01-js-ctypes.diff
Patch2:                  spidermonkey-02-jsfunc.diff
Patch3:                  spidermonkey-03-methodjit-sparc.diff
Patch4:                  spidermonkey-04-jemalloc.diff
Patch5:                  spidermonkey-05-pgo-ss12_2.diff
Patch6:                  spidermonkey-06-use-system-libffi.diff
Patch7:                  spidermonkey-07-makefile.diff
# see b.g.o 619721 and 595447
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWprd
RequireS: SUNWpr
BuildRequires: SUNWzip

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
%setup -q -n js-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
export LDFLAGS="-B direct -z ignore"
export CFLAGS="-xlibmopt"
export OS_DEFINES="-D__USE_LEGACY_PROTOTYPES__"
export CXXFLAGS="-xlibmil -xlibmopt -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"

cd js/src
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --with-nspr-cflags='-I/usr/include/mps'   \
            --with-nspr-libs="-L/usr/lib/mps -lnspr4" \
            --enable-threadsafe
make

%install

cd js/src
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%changelog
* Thu Oct 20 2011 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
