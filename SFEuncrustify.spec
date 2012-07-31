#
# spec file for package SFEuncrustify.spec
#
# includes module(s): uncrustify
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	uncrustify

Name:		SFEuncrustify
IPS_Package_Name:	developer/uncrustify
Version:	0.59
Summary:	Reformat Source
Group:		Development/Tools
License:	GPLv2
URL:		http://uncrustify.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Source Code Beautifier for C, C++, C#, D, Java, and Pawn

%prep
%setup -q -n %{src_name}-%{version}

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

./configure --prefix=%{_prefix}

make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -m644 man/%{src_name}.1 $RPM_BUILD_ROOT/%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{src_name}
cp -r documentation/* $RPM_BUILD_ROOT/%{_docdir}/%{src_name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc COPYING AUTHORS README NEWS
%{_bindir}/%{src_name}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}
%{_mandir}/man1/%{src_name}.1


%changelog
* Sun Dec 11 2011 - Milan Jurik
- bump to 0.59
* Tue Jun 15 2010 - Milan Jurik
- initial import to SFE
