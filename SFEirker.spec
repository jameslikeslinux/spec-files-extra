#
# spec file for package SFEirker
#
# includes module(s): irker
#
#
#

##TODO## make SMF manifest for irkerd

%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEirker
Summary:		 An IRC client that runs as a daemon accepting notification requests as JSON objects presented to a listening socket
Version:                 1.12
Source:                  http://www.catb.org/~esr/irker/irker-%{version}.tar.gz
##TODO## temporary patch
Patch1:			 irker-1.12-urlparse.diff
URL:                     http://www.catb.org/esr/irker
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
License:		BSD

%include default-depend.inc
Requires:                  %{pnm_requires_python_default}
BuildRequires:             %{pnm_buildrequires_python_default}

#irclib in perl


%prep
%setup -q -n irker-%{version}

#replace with explicit python version from %{python_major_minor_version}
perl -pi -e 's:^#! */usr/bin/python.*:#!/usr/bin/python%{python_major_minor_version}:' `find . -type f -print`
perl -pi -e 's:^#! */usr/bin/env *python:#!/usr/bin/python%{python_major_minor_version}:' `find . -type f -print`

%patch1 -p1

%build


%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755              $RPM_BUILD_ROOT/%{_bindir}
install -m    0755 irkerd       $RPM_BUILD_ROOT/%{_bindir}/irkerd
install -m    0755 irk          $RPM_BUILD_ROOT/%{_bindir}/irk
install -m    0755 irkerhook.py $RPM_BUILD_ROOT/%{_bindir}/irkerhook.py

install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}
install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}/irker

for file in COPYING Makefile NEWS README filter-example.py filter-test.py hacking.txt install.txt irker-logo.png irkerd.service irkerd.xml irkerhook.xml org.catb.irkerd.plist security.txt
 do
##TODO## be next time more nice to executable scripts, okay?
 install            $file $RPM_BUILD_ROOT/%{_docdir}/irker/$file
 done


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/irker
%{_docdir}/irker/*




%changelog
* Thu Oct 25 2012 - Thomas Wagner
- initial spec
- use patch1 until code base includes fix for lazy urlparse
  which can't decode irc://
