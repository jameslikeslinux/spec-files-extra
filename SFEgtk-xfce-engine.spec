#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name gtk-xfce-engine
%define src_url http://archive.xfce.org/xfce/4.8/src/

Name:		SFEgtk-xfce-engine
Summary:	Port of xfce engine to GTK+-2.0
Version:	2.8.0
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Group:		User Interface/Desktops
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs
BuildRequires:	SFExfce4-dev-tools

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
	--bindir=%{_bindir}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-gtk-doc		\
	--disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete libtool .la files
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/libxfce.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/themes*

%changelog
* Sat Mar 26 2011 - Milan Jurik
- bump to 2.8.0, move to SFE from osol xfce
* Tue Aug 03 2010 - brian.cameron@oracle.com
- Bump to 2.6.0.
* Sun Dec 09 2007 - sobotkap@centrum.cz
- Bump to 2.4.2 version
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
- Version bumped to 2.4.1
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
