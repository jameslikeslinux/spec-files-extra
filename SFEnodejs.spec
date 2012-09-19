#
# spec file for package SFEnodejs
#
# includes module(s): nodejs
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Summary:	Asynchronous JavaScript Engine  
Name:		SFEnodejs  
IPS_Package_Name:	runtime/javascript/nodejs
Version:	0.8.8
License:	BSD  
Group:		System/Libraries  
URL:		http://nodejs.org/  
Source:		http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz  
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
BuildRequires: SFEgcc
Requires: SFEgccruntime

%description  
Node's goal is to provide an easy way to build scalable network  
programs. In the above example, the two second delay does not prevent  
the server from handling new requests. Node tells the operating system  
(through epoll, kqueue, /dev/poll, or select) that it should be  
notified when the 2 seconds are up or if a new connection is made --  
then it goes to sleep. If someone new connects, then it executes the  
callback, if the timeout expires, it executes the inner callback. Each  
connection is only a small heap allocation.  

%package devel  
Summary:	Development headers for nodejs  
Group:		Development/Libraries  

%description devel  
Development headers for nodejs.  

%prep  
%setup -q -n node-v%{version}  

%build  
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} \
	--shared-openssl

make -j$CPUS

%install  
rm -rf $RPM_BUILD_ROOT  
export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
make install DESTDIR=$RPM_BUILD_ROOT

%clean  
rm -rf $RPM_BUILD_ROOT  
  
%files  
%defattr(-, root, bin)
%doc AUTHORS ChangeLog LICENSE
%{_bindir}/node
%{_bindir}/npm
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}
%{_libdir}/node
%{_libdir}/node_modules
%{_libdir}/dtrace/node.d

%files devel  
%defattr(-, root, bin)  
%{_bindir}/node-waf
%{_includedir}/node  

%changelog  
* Thu Aug 30 2012 - Milan Jurik
- bump to 0.8.8
* Fri Jul 27 2012 - Milan Jurik
- bump to 0.8.4
* Wed May 16 2012 - Milan Jurik
- bump to 0.6.18
* Sat Dec 31 2011 - Milan Jurik
- bump to 0.6.6
* Sat Nov 19 2011 - Milan Jurik
- bump to 0.6.2
* Thu Jun 30 2011 - Milan Jurik
- bump to 0.4.9
* Thu Mar 24 2011 - Thomas Wagner
- bump to 0.4.3
* Sat Mar 05 2011 - Milan Jurik
- bump to 0.4.2, use internal libev
* Wed Jan 05 2011 - Milan Jurik
- bump to 0.2.6
* Sun Nov 28 2010 - Milan Jurik
- bump to 0.2.5
* Fri Nov 12 2010 - Milan Jurik
- bump to 0.2.4
* Sat Oct 16 2010 - Milan Jurik
- bump to 0.2.3
* Thu Sep 07 2010 - Milan Jurik
- initial spec
