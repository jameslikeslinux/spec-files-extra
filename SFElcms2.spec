#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name lcms2

Name:		SFElcms2
IPS_Package_Name:	library/lcms2
Summary:	A little color management system
Version:	2.2
URL:		http://www.littlecms.com/
Source:		http://www.littlecms.com/%{src_name}-%{version}.tar.gz
License:	MIT
SUNW_Copyright:	lcms2.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --docdir=%{_docdir}

make -j$CPUS

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/lib*a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, sys) %{_datadir}
%{_bindir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_mandir}/*
%{_includedir}/*

%changelog
* Sat Nov  5 2011 - Pavel Heimlich
- initial spec
