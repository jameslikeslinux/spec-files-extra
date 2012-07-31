#
# spec file for package SFEzziplib.spec
#
# includes module(s): zziplib
#
%include Solaris.inc

%define src_name	zziplib

Name:		SFEzziplib
IPS_Package_Name:	library/zziplib
Summary:	ZZIPlib library
Version:                0.13.60
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.bz2
URL:		http://zziplib.sourceforge.net/
License:	LGPLv2.1+
Patch1:		zziplib-01-ldflags.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
autoconf
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Sat Oct 29 2011 - Milan Jurik
- bump to 0.13.60
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
