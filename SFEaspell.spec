#
# spec file for package SFEaspell
#
# includes module(s): aspell
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname aspell

Name:                    SFEaspell
IPS_Package_Name:	 text/aspell
Summary:                 Aspell - GNU Aspell is a Free and Open Source spell checker
Group:                   Utility
Version:                 0.60.6.1
URL:		         http://aspell.net
License: 		 GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:           SFEaspell-core
Requires:           SFEaspell-dict-en

%description
GNU Aspell is a Free and Open Source spell checker designed to
eventually replace Ispell. It can either be used as a library or as an
independent spell checker. Its main feature is that it does a superior
job of suggesting possible replacements for a misspelled word than
just about any other spell checker out there for the English
language. Unlike Ispell, Aspell can also easily check documents in
UTF-8 without having to use a special dictionary. Aspell will also do
its best to respect the current locale setting. Other advantages over
Ispell include support for using multiple dictionaries at once and
intelligently handling personal dictionaries when more than one Aspell
process is open at once.

%changelog
* Wed Feb 22 2012- logan@gedanken.org
- Initial spec.
