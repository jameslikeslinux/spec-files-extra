#
# spec file for package SFEmod-wsgi
#
# includes module(s): mod_wsgi
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use mod_wsgi_64 = mod_wsgi.spec
%endif

%include base.inc
%use mod_wsgi = mod_wsgi.spec

Name:		SFEmod-wsgi
IPS_Package_Name:	web/server/apache-22/module/mod-wsgi
Version:	%{mod_wsgi.version}
Summary:	%{mod_wsgi.summary}
Group:		System Environment/Daemons
License:	Apache v2
URL:		%{mod_wsgi.url}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgawk
BuildRequires:	SUNWgnome-common-devel
BuildRequires:	SUNWapch22u
Requires:	SUNWapch22u
Requires:	SUNWscpu

%description
The aim of mod_wsgi is to implement a simple to use Apache module which can host any Python application which supports the Python WSGI interface. The module would be suitable for use in hosting high performance production web sites, as well as your average self managed personal sites running on web hosting services. 

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%mod_wsgi_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%mod_wsgi.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
%mod_wsgi_64.build -d %name-%version/%_arch64
%endif

%mod_wsgi.build -d %name-%version/%{base_arch}


%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%mod_wsgi_64.install -d %name-%version/%_arch64
%endif

%mod_wsgi.install -d %name-%version/%{base_arch}


%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_prefix}/apache2/2.2/libexec/mod_wsgi.so
%ifarch amd64 sparcv9
%{_prefix}/apache2/2.2/libexec/%{_arch64}/mod_wsgi.so
%endif

%changelog
* Sat Mar 26 2011 - Milan Jurik
- initial spec
