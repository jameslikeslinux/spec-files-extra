#
# spec file for package SFEofflineimap
#
# includes module(s): offlineimap
#
%include Solaris.inc

%define version_suffix g37d0fe8
%define build_dir_suffix 64c2baa

Name:		SFEofflineimap
Summary:	Bi-directional syncing of IMAP/Maildir email boxes
Version:	6.3.2.1
Group:		Applications/Internet
Source:		http://download.github.com/nicolas33-offlineimap-v%{version}-0-%{version_suffix}.tar.gz
URL:		http://offlineimap.org/
License:	GPLv2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
Requires: SUNWPython

%prep
%setup -q -n nicolas33-offlineimap-%{build_dir_suffix}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
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
