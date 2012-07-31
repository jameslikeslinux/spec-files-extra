#
# spec file for package SFEyasm.spec
#
# includes module(s): yasm
#
%include Solaris.inc

%define src_name	yasm
%define src_url		http://www.tortall.net/projects/yasm/releases

Name:                   SFEyasm
IPS_Package_Name:	developer/yasm
Summary:                Yet another assembler
Version:                1.2.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
License:		LGPL
SUNW_Copyright:		yasm.copyright
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%{_libdir}

%changelog
* Thu Jun 21 2012 - Milan Jurik
- bump to 1.2.0
* Sun Oct 16 2011 - Milan Jurik
- add IPS package name
* Thu Nov 4 2010 - Alex Viskovatoff
- Update to 1.1.0
* Wed Jun 2 2008 - oboril.lukas@gmail.com
- bump to 0.7.1
- remove CFLAGS, LDFLAGS, use wihtout optim flags is
 the safest way to have correct yasm.
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial version
