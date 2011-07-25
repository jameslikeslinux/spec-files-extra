#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name xfce4-dev-tools
%define src_url http://archive.xfce.org/xfce/4.8/src/

Name:		SFExfce4-dev-tools
Summary:	Xfce Development Tools
Version:	4.8.0
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Group:		User Interface/Desktops
License:	GPLv2
SUNW_Copyright: xfce4-dev-tools.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
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
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xfce4*

%changelog
* Mon Jul 25 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Sun Mar 20 2011 - Milan Jurik
- bump to 4.8.0, move to SFE from osol xfce
* Tue Aug 03 2010 - brian.cameron@oracle.com
- Bump to 4.6.0
* Wed Aug 19 2009 - sobotkap@gmail.com
- Added IPS meta-tags required by juicer.
* Sat Feb 28 2009 - sobotkap@gmail.com
- Clean svn build method as we don't build from svn anymore
- As version use main version of Xfce release (defined in prod.inc)
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Thu Apr  5 2007 - dougs@truemail.co.th
- Initial version
