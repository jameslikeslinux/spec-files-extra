Name:		SFEmod-wsgi
Version:	3.3
Summary:	mod_wsgi implements a simple to use Apache module for Python WSGI
License:	Apache v2.0
URL:		http://www.modwsgi.org/
Source:		http://modwsgi.googlecode.com/files/mod_wsgi-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n mod_wsgi-%{version}

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --with-apxs=%{_bindir}/apxs

make

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%changelog
* Sat Mar 26 2011 - Milan Jurik
- initial spec
