



#http://pypi.python.org/packages/source/i/irc/irc-3.4.1.zip




#
# spec file for package SFEirc
#
# includes module(s): irc
#
#
#

# please don't do version bumps without testing against SFEirker.spec ! 

%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEpyirclib
IPS_Package_Name:	 library/python-2/irclib
Summary:		 IRC (Internet Relay Chat) protocol client library for Python
# please don't do version bumps without testing against SFEirker.spec ! 
Version:                 3.4.1
Source:                  http://pypi.python.org/packages/source/i/irc/irc-%{version}.zip
URL:                     http://pypi.python.org/pypi/irc/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                  %{pnm_requires_python_default}
BuildRequires:             %{pnm_buildrequires_python_default}


%prep
%setup -q -n irc-%{version}

#replace with explicit python version from %{python_major_minor_version}
perl -pi -e 's:^#! */usr/bin/python.*:#!/usr/bin/python%{python_major_minor_version}:' `find . -type f -print`
perl -pi -e 's:^#! */usr/bin/env *python:#!/usr/bin/python%{python_major_minor_version}:' `find . -type f -print`

%build
python%{python_version} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*


%changelog
* Wed Oct 24 2012 - Thomas Wagner
- initial spec
