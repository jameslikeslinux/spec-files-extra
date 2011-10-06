#
# spec file for package SFElibcddb
#
# includes module(s): libcddb
#

%include Solaris.inc

%define	src_name libcddb

Name:		SFElibcddb
IPS_Package_Name:	library/audio/libcddb 
Summary:	C library to access data on a CDDB server
Group:		System/Libraries
Version:	1.3.2
License:	LGPLv2
SUNW_Copyright:	libcddb.copyright
URL:		http://libcddb.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SFElibiconv
BuildRequires:	SFElibiconv-devel

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
Requires:	%name

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

libtoolize --copy --force
#aclocal needed otherwise version mismatch
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -f
autoconf -f
./configure --prefix=%{_prefix}           \
            --bindir=%{_bindir}           \
            --libdir=%{_libdir}           \
            --includedir=%{_includedir}   \
            --mandir=%{_mandir}           \
            --infodir=%{_infodir}         \
            --disable-static              \
            --enable-shared               \
            --without-cdio

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

#Move cddb_query example to demo directoty
install -d $RPM_BUILD_ROOT%{_prefix}/demo/libcddb/bin
mv $RPM_BUILD_ROOT%{_bindir}/cddb_query \
                  $RPM_BUILD_ROOT%{_prefix}/demo/libcddb/bin/cddb_query
rmdir $RPM_BUILD_ROOT%{_bindir}

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
%{_prefix}/demo/libcddb/bin/cddb_query

%changelog
* Thu Oct 06 2011 - Milan Jurik
- clean up, add IPS package name
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sun Dev 21 2008 - Thomas Wagner
- changed ACLOCAL_FLAGS to conditionally use m4 files from CBEgettext location (/opt/dtbld or /opt/jdsbld, ..) bcs. missing AM_GNU_GETTEXT_VERSION|AM_ICONV when using jds cbe 1.7.0(-rc1)
* Tue Sep 02 2008 - halton.huo@sun.com
- Remove empty %{_bindir}
* Sun Aug 17 2008 - nonsea@users.sourceforge.net
- Remove /usr/gnu/share/aclocal from ACLOCAL_FLAGS to fix build issue
* Fri Jul 11 2008 - andras.barna@gmail.com
- Add ACLOCAL_FLAGS, SFElibiconv dep
* Mon Feb 04 2008 - Michal dot Pryc [(at] Sun . Com
- cddb_query is an example utlility. Moved to devel package, now it is installed
  under /usr/demo/libcddb/bin/cddb_query
- build without cdio support. Affects only cddb_query example utility.
* Sat Jul 14 2007 - dougs@truemail.co.th
- Initial spec
