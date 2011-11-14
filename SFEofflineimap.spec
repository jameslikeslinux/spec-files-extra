#
# spec file for package SFEofflineimap
#
# includes module(s): offlineimap
#
%include Solaris.inc
%include packagenamemacros.inc

%define build_dir_suffix 94450e9

Name:		SFEofflineimap
Summary:	Bi-directional syncing of IMAP/Maildir email boxes
Version:	6.3.4
Group:		Applications/Internet
Source:		http://githubredir.debian.net/github/nicolas33/offlineimap/v%{version}.tar.gz
URL:		http://offlineimap.org/
License:	GPLv2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:  %{pnm_buildrequires_python_default}
Requires:       %{pnm_requires_python_default}

%prep
%setup -q -n nicolas33-offlineimap-%{build_dir_suffix}

%build
/usr/bin/python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
/usr/bin/python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Wed Aug 10 2011 - Knut Anders Hatlen
- Bump to 6.3.4
- Use packagenamemacros.inc for Python version
* Fri May 13 2011 - Knut Anders Hatlen
- Fix Python 2.6 dependencies
* Wed Mar 23 2011 - Knut Anders Hatlen
- Bump to 6.3.2.1
- Remove upstream patch
* Tue Aug 31 2010 - Knut Anders Hatlen
- Add patch http://article.gmane.org/gmane.mail.imap.offlineimap.general/1841
* Wed Aug 25 2010 - Milan Jurik
- bump to 6.2.0.2 
* Sat Mar 31 2007 - Eric Boutilier
- Initial spec
- Python App: Two-way sync of IMAP/Maildir email boxes
