#
# spec file for package SFEsnappy
#
# includes module(s): snappy
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname snappy

Name:                    SFEsnappy
IPS_Package_Name:	 compress/snappy
Summary:                 snappy - A fast compressor/decompressor
Group:                   Utility
Version:                 1.0.5
URL:		         http://code.google.com/p/snappy/
Source:		         http://snappy.googlecode.com/files/snappy-%{version}.tar.gz
License: 		 New BSD License
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Snappy is a compression/decompression library. It does not aim for
maximum compression, or compatibility with any other compression
library; instead, it aims for very high speeds and reasonable
compression. For instance, compared to the fastest mode of zlib,
Snappy is an order of magnitude faster for most inputs, but the
resulting compressed files are anywhere from 20% to 100% bigger. On a
single core of a Core i7 processor in 64-bit mode, Snappy compresses
at about 250 MB/sec or more and decompresses at about 500 MB/sec or
more.

Snappy is widely used inside Google, in everything from BigTable and
MapReduce to our internal RPC systems. (Snappy has previously been
referred to as “Zippy” in some presentations and the likes.)

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libsnappy.*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/snappy
%{_datadir}/doc/snappy/*

%changelog
* Sat Apr 28 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
