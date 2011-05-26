#
# spec file for package SFEtexi2html
#
# includes module: texi2html
#

# text/texinfo supplies /usr/bin/texi2html
%define _basedir /usr/gnu
%include Solaris.inc
%define srcname texi2html

Name: SFEtexi2html
Version: 5.0
Release: 1
# GPLv2+ is for the code
# OFSFDL (Old FSF Documentation License) for the documentation
# CC-BY-SA or GPLv2 for the images
License: GPLv2+ and OFSFDL and (CC-BY-SA or GPLv2)
Group: Applications/Text
Summary: A highly customizable texinfo to HTML and other formats translator
Source0: http://download.savannah.nongnu.org/releases/%{srcname}/%{srcname}-%{version}.tar.bz2
URL: http://www.nongnu.org/texi2html/
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
# perl is picked up automatically in most cases and the package may have 
# a different name so it is better not to require it. Moreover such old perl
# is unlikely to show up in a rpm based distribution.
#Requires: perl >= 5.004
#Requires: latex2html
#BuildRequires: perl(Text::Unidecode) 
# not detected automatically because it is required at runtime based on
# user configuration
#Requires: perl(Text::Unidecode)
#BuildArch: noarch
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%description
The basic purpose of texi2html is to convert Texinfo documents into HTML,
and other formats.  Configuration files written in Perl provide a fine degree
of control over the final output, allowing most every aspect of the final
output not specified in the Texinfo input file to be specified.

%prep
%setup -q -n %srcname-%version

%build
%configure --prefix=%_prefix
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
mkdir $RPM_BUILD_ROOT/%_datadir/doc

#ln -s texi2any $RPM_BUILD_ROOT%{_bindir}/texi2html

rm -rf __dist_examples
mkdir -p __dist_examples
cp -a examples __dist_examples
rm -f __dist_examples/examples/Makefile*

# directories shared by all the texinfo implementations for common
# config files, like htmlxref.cnf
#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/texinfo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_datadir/doc
%doc AUTHORS COPYING ChangeLog NEWS README TODO %{srcname}.init
#%doc __dist_examples/examples/
%{_bindir}/%{srcname}
#%{_bindir}/texi2any
%{_mandir}/man*/%{srcname}*
%{_infodir}/%{srcname}.info*
%dir %{_datadir}/texinfo/
%dir %{_datadir}/texinfo/init
%{_datadir}/texinfo/init/*.init
%{_datadir}/texinfo/html/%{srcname}.html
%attr (-, root, other) %_datadir/locale
%dir %{_datadir}/%{srcname}/i18n/
%{_datadir}/%{srcname}/i18n/*
%dir %{_datadir}/%{srcname}/images/
%{_datadir}/%{srcname}/images/*
%{_datadir}/%{srcname}/lib/*
#%dir %{_sysconfdir}/texinfo

%changelog
* Sun May 15 2011 Alex Viskovatoff
- adapt spec from source tarball to SFE
* Sun Sep  9 2007 Patrice Dumas <pertusus@free.fr> 5.0-1
- update to 5.0
* Mon Nov 14 2005 Patrice Dumas <pertusus@free.fr> 1.77-1
- cleanups
* Mon Mar 23 2004 Patrice Dumas <pertusus@free.fr> 0:1.69-0.fdr.1
- Initial build.
