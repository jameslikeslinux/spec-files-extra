#
# spec file for package SFEsugar-storybuilder
#
# includes module(s): sugar-storybuilder
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEsugar-storybuilder
Summary:                 Sugar StoryBuilder
URL:                     http://www.sugarlabs.org/
Version:                 19 
Source:                  http://download.sugarlabs.org/sources/honey/StoryBuilder/StoryBuilder-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SFEsugar
BuildRequires:           SFEsugar
Requires: 		 SFEsugar-toolkit
BuildRequires: 		 SFEsugar-toolkit
#
#This project requiress Python Mozilla bindings (PyXPCOM) that enables Python to
#used inside of Mozilla applications like XULRunner. 
#
#Requires: 		 python-pygame
#BuildRequires:		 python-xpcom192
#BuildRequires:		 mozilla-xulrunner192

%if %build_l10n
%package l10n
Summary:      %{summary} - l10n files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:     %{name}
%endif

%prep
%setup -q -n StoryBuilder-%version

%build
export PYTHON=/usr/bin/python%{pythonver}
python%{pythonver} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install --prefix=$RPM_BUILD_ROOT/usr

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

# replace the old scripts with script files
%post
%restart_fmri gconf-cache desktop-mime-cache icon-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/sugar

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %{_datadir}/sugar/activities/StoryBuilder.activity
%{_datadir}/sugar/activities/StoryBuilder.activity/*
%{_datadir}/locale/bi
%{_datadir}/locale/bi/LC_MESSAGES
%{_datadir}/locale/cpp
%{_datadir}/locale/cpp/LC_MESSAGES
%{_datadir}/locale/na
%{_datadir}/locale/na/LC_MESSAGES
%endif

%changelog
* Sat Nov 19 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 19
* Tue Sep 27 2011 - Ken Mays <kmays2000@gmail.com>
- Requires Pygame & PyXPCOM
- Created with 15.
