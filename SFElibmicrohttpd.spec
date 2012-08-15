# adapted from a source prm found on http://rpm.pbone.net

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc


Name:		SFElibmicrohttpd
IPS_package_name:  library/libmicrohttpd
Version:	0.9.21

Summary:	Small Embeddable HTTP Server Library
License:	GNU LGPL v2.1
Group:		Development/Libraries
Url:		http://gnunet.org/libmicrohttpd/

Source:		http://ftpmirror.gnu.org/libmicrohttpd/libmicrohttpd-%{version}.tar.gz
##TODO##Source1:	%{name}.copyright

SUNW_BaseDir:        %{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

##TODO## BuildRequires:	libcurl-devel
##TODO## BuildRequires:	libgcrypt-devel
##TODO## BuildRequires:	libtasn1-devel
BuildRequires:	SUNWgnutls-devel
Requires: 	SUNWgnutls
BuildRequires:	SUNWlibgcrypt-devel
Requires:	SUNWlibgcrypt
BuildRequires:	SFEgcc
Requires:	SFEgccruntime



%description
GNU libmicrohttpd is a small C library that is supposed to make it easy to run an HTTP server as part of another application. GNU libmicrohttpd is free software and part of the GNU project. Key features that distinguish libmicrohttpd from other projects are:

    * C library: fast and small
    * API is simple, expressive and fully reentrant
    * Implementation is http 1.1 compliant
    * HTTP server can listen on multiple ports
    * Support for IPv6
    * Support for incremental processing of POST data
    * Creates binary of only 30k (without TLS/SSL support)
    * Three different threading models
    * Supported platforms include GNU/Linux, FreeBSD, OpenBSD, NetBSD, OS X, W32, Symbian and z/OS
    * Optional support for SSL3 and TLS (requires libgcrypt)

libmicrohttpd was started because the author needed an easy way to add a concurrent HTTP server to other projects. Existing alternatives were either non-free, not reentrant, standalone, of terrible code quality or a combination thereof. Do not use libmicrohttpd if you are looking for a standalone http server, there are many other projects out there that provide that kind of functionality already. However, if you want to be able to serve simple WWW pages from within your C or C++ application, check it out.

%prep
%setup -q -n libmicrohttpd-%version

#perl -w -pi.bak -e "s,.{wl}-soname .wl.soname,,; s,-soname .soname,," configure


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags} -pthreads"
export LDFLAGS="%{_ldflags} -pthreads  -lnsl"
export LD=ld-wrapper

#aclocal
#libtoolize --copy --force
#automake -a -f
#autoconf -f

%configure --prefix=%{_prefix} \
           --mandir=%{_mandir} \
	   --enable-curl \
	   --enable-messages \
	   --enable-https \
	   --enable-client-side \
           --disable-static

gmake -j$CPUS

%install

gmake install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \; -o -name '*.a'  -exec rm {} \;

rm -f $RPM_BUILD_ROOT%{_infodir}/dir


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libmicrohttpd.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sat Jul 21 2012 - Thomas Wagner
- bump to 0.9.21
* Thu May 17 2012 - Thomas Wagner
- initial spec (adapted from http://rpm.pbone.net)

