#
# spec file for package SFElibntlm
#
# includes module(s): libntlm
#
%include Solaris.inc

%define	src_name libntlm
%define	src_url	http://www.nongnu.org/libntlm/releases

Name:		SFElibntlm
IPS_Package_Name:	library/security/libntlm
Summary:	Microsoft's NTLM authentication library
Version:	1.3
Group:		System/Libraries
License:	LGPLv2.1+
URL:		http://www.nongnu.org/libntlm/
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Dec 12 2011 - Milan Jurik
- bump to 1.3
* Sun Feb 13 2011 - Milan Jurik
- bump to 1.2
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
