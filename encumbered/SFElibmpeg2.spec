#
# spec file for package SFElibmpeg2
#
# includes module(s): libmpeg2
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name libmpeg2
%define	src_url	http://libmpeg2.sourceforge.net/files

Name:                SFElibmpeg2
Summary:             MPEG2 Decoder library
URL:                 http://libmpeg2.sourceforge.net
License:             GPLv2
SUNW_Copyright:	     libmpeg2.copyright
Version:             0.5.1
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_bindir}
%{_mandir}/man1

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Jul 21 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Wed Feb 02 2011 - Alex Viskovatoff
- Update to 0.5.1
- Don't call autoconf explicitly: that breaks the build
- Use cc_is_gcc and %optflags
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Change build flags and remove unnecessary autofoo calls.
* Sat Jul 14 2007 - dougs@truemail.co.th
- Initial spec
