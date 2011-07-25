#
# spec file for package SFEvala
#
# includes module(s): vala
#
%include Solaris.inc

%define	src_name vala
%define	src_url	http://download.gnome.org/sources/vala/0.12

Name:                SFEvala
Summary:             Vala programming language
Version:             0.12.0
URL:                 http://live.gnome.org/Vala
Source:              %{src_url}/%{src_name}-%{version}.tar.bz2
License:	     GPLv2
SUNW_Copyright:	     vala.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional runtime
requirements and without using a different ABI compared to applications and
libraries written in C.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
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

aclocal
libtoolize --copy --force 
automake -a -f
autoconf -f 
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
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/devhelp
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/vala.*
%{_datadir}/vala-0.12/vapi/*
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Jul 25 2011 - N.B.Prashanth
- add SUNW_Copyright
* Sat May 14 2011 - nbprashanth <nbprash.mit@gmail.com>
- Bump to 0.12.0.
* Wed Mar 10 2010 - brian.cameron@sun.com
- Bump to 0.7.10.
* Tue Nov 24 2009 - brian.cameron@sun.com
- Bump to 0.7.8.
* Sun Oct 11 2009 - brian.cameron@sun.com
- Bump to 0.7.7.
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
