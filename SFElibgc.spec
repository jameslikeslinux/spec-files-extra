#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name gc
%define src_url http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/

Name:		SFElibgc
Summary: 	The Boehm-Demers-Weiser conservative garbage collector
Version: 	7.1
URL: 		http://www.hpl.hp.com/personal/Hans_Boehm/gc/
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Group: 		Development/Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot: 	%{_tmppath}/%{name}-root
%include default-depend.inc

%description
The Boehm-Demers-Weiser conservative garbage collector can be used as a garbage collecting replacement for C malloc or C++ new. It allows you to allocate memory basically as you normally would, without explicitly deallocating memory that is no longer useful. The collector automatically recycles memory when it determines that it can no longer be otherwise accessed.

%package devel
Summary:	%{summary} - developer files
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-cplusplus		\
	--enable-large-config		\
	--enable-shared			\
	--disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete libtool .la files
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_libdir}/lib*.so*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gc
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%{_includedir}

%changelog
* Mon Mar 21 2011 - Milan Jurik
- initial spec
