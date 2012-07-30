# spec file for package SFEpython-nn-tornado
#
# automatic packagename by platform default python version
#
# includes module(s): Tornado
#
%include Solaris.inc
%include packagenamemacros.inc

%define src_url         http://github.com/downloads/facebook
%define src_name        tornado

#2.3.1 2.3
%define src_version	2.3
#2.3   2.3
%define src_version_major_minor 2.3
%define packagename SFEpython%{python_version_package_string}-%{src_name}

Name:		%{packagename}
##TODO## check IPS package naming conventions for SFE
IPS_Package_Name:	web/python/%{src_name}
Version:	%{src_version}
Summary:	A high-level Python Web framework that enables Rapid Development
License:	Apache 2.0
##TODO## set group to something webserver made in python    Group:		Development/Languages/Python
URL:		http://www.tornadoweb.org/
Source:		%{src_url}/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	%{pnm_buildrequires_python_default}
Requires:	%{pnm_requires_python_default}

%description
Webserver for Python Applications implementd in Python.
Use e.g. with Django framework.
Test:
make a file with the content below, chmod +x and run it. Then
make a http request on http://ipaddress:8888

#!/usr/bin/python%{python_version}
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


%prep
%setup -q -n %{src_name}-%{version}

%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=%{buildroot} --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p %{buildroot}%{_libdir}/python%{python_version}/vendor-packages
mv %{buildroot}%{_libdir}/python%{python_version}/site-packages/* \
   %{buildroot}%{_libdir}/python%{python_version}/vendor-packages/
rmdir %{buildroot}%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Sun Jun 10 2012 - Thomas Wagner
- Initial Version
