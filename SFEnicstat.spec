#
# spec file for package SFEnicstat
#
%include Solaris.inc
Name:		SFEnicstat
IPS_Package_Name:	system/network/nicstat
Summary:	tool for displaying network load similar to iostat/prstat
URL:		http://blogs.oracle.com/timc/entry/nicstat_the_solaris_network_monitoring
Version:	1.90
Source:                  nicstat-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc


%prep
%setup  -q -n nicstat-%version
cp -p Makefile.Solaris Makefile

%build

#nothing to configure, just "compile" it with make
make


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp -p .nicstat.`uname -o`_`uname -r | sed -e 's/5\.//'`_`uname -p` $RPM_BUILD_ROOT/%{_bindir}/nicstat

##TODO## install Man pages, ...

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*


%changelog
* Mon Dec 12 2011 - Thomas Wagner
- merge with svn
- IPS_package_name by jurikm 2011-12-11
* Tue Nov  8 2011 - Thomas Wagner
- bump to 1.90
- change to new build style, update to new source tarball
* Thu Apr 29 2011 - Thomas Wagner
- bump to 1.90, rework handling of new tarball, install only binary no scripts
* Mon Jul 20 2009 - matt@greenviolet.net
- Update Source URL
* Sun Jun 01 2008 - trisk@acm.jhu.edu
- Don't hardcode /usr/bin
* Wed Jan 02 2008 - Thomas Wagner
- Initial spec
