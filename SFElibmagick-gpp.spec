#
# spec file for package SFEimagemagick.spec
#
# includes module(s): imagemagick
#
%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	ImageMagick
#%define src_url		ftp://ftp.imagemagick.org/pub/ImageMagick
#upstream does not keep old versions, provide alternate url:
%define src_url                http://ftp.sunet.se/pub/multimedia/graphics/ImageMagick
%define major		6.7.6
%define minor		10

Name:                   SFElibmagick-gpp
IPS_Package_Name:	image/library/g++/imagemagick
Summary:                Image Manipulation Libraries
Version:                %{major}.%{minor}
License:                ImageMagick License
SUNW_Copyright:         imagemagick.copyright
Source:                 %{src_url}/%{src_name}-%{major}-%{minor}.tar.bz2
Group:			Graphics
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFEjasper-devel
Requires:	SFEjasper
BuildRequires:	SFElibwebp-devel
Requires:	SFElibwebp
Requires:	SFEimagemagick

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{major}-%{minor}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++ 
export CPPFLAGS="-I/usr/include/freetype2 -I/usr/X11/include"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib"
export CFLAGS="%optflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-perl=no		\
            --enable-shared		\
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a
find $RPM_BUILD_ROOT%{_libdir} -name lib\*.\*a -exec rm {} \;

rm -rf $RPM_BUILD_ROOT%{_bindir}
rm -rf $RPM_BUILD_ROOT%{_datadir}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/%{src_name}-%{major}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Jun 23 2012 - Logan Bruns <logan@gedanken.org>
- updated to 6.7.6-10
- switched buildrequires from SUNWimagick to SFEimagemagick
* Sun Apr 01 2012 - Pavel Heimlich
- source url
* Fri Dec 30 2011 - Milan Jurik
- fork from SFEimagemagick for g++ libs
* Thu Dec 8 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.3-10
* Wed Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.2-6
* Wed Aug 24 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.1-10
* Fri Jul 29 2011 - Alex Viskovatoff
- Add missing (build) dependency
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jul 03 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.0-10
* Mon Jun 06 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.0-4
* Tue Apr 12 2011 - Alex Viskovatoff
- update to 6.6.9-4
* Thu Jan 13 2010 - Milan Jurik
- bump to 6.6.7-0
* Thu Nov 26 1009 - Thomas Wagner
- bump to 6.5.8-0
- new download-URL
- changed include path /usr/include/freetype2
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Bump version to 6.3.6-10.
- Add check to prevent build using Gcc.
- Add dependency on Perl.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Bump to 6.3.6-9.
* Tue Jul 10 2007 - brian.cameron@sun.com
- Bump to 6.3.5.  Remove the -xc99=%none from CFLAGS since
  it is breaking the build.
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version - version in sfw is too old :(
