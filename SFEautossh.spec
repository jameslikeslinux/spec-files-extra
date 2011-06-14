#
# spec file for package: autossh
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc

%define src_version 1.4b

Name:		SFEautossh
Version:	1.4.2
Summary:	Automatically restart SSH sessions and tunnels
License:	BSD
Url:		http://www.harding.motd.ca/autossh/
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright

Source0:	http://www.harding.motd.ca/autossh/%{sname}-%{src_version}.tgz

%include default-depend.inc
BuildRequires:	SUNWsshu
Requires:	SUNWsshu

Meta(info.maintainer):          James Lee <jlee@thestaticvoid.com>
Meta(info.upstream):            Carson Harding <harding@motd.ca>
Meta(info.upstream_url):        http://www.harding.motd.ca/autossh/
Meta(info.classification):	org.opensolaris.category.2008:System/Security

%description
autossh is a program to start a copy of ssh and monitor it, restarting it as
necessary should it die or stop passing traffic. The idea is from rstunnel
(Reliable SSH Tunnel), but implemented in C. 

%prep
%setup -q -n %{sname}-%{src_version}

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
./configure --prefix=$RPM_BUILD_ROOT%{_prefix} --mandir=$RPM_BUILD_ROOT%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install

mv -f $RPM_BUILD_ROOT%{_datadir}/examples/autossh $RPM_BUILD_ROOT%{_docdir}/autossh/examples
rm -rf $RPM_BUILD_ROOT%{_datadir}/examples

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}/autossh
%attr(755,root,sys) %dir %{_datadir}
%{_mandir}/man1/autossh.1
%attr(755,root,other) %dir %{_docdir}
%{_docdir}/autossh

%changelog
* Mon Jun 13 2011 - jlee@thestaticvoid.com
- Update for SFE inclusion. 
* Mon Apr 18 2011 - jlee@thestaticvoid.com
- Initial version
