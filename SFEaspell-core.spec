#
# spec file for package SFEaspell-core
#
# includes module(s): aspell-core
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname aspell

Name:                    SFEaspell-core
IPS_Package_Name:	 text/aspell-core
Summary:                 Aspell - GNU Aspell is a Free and Open Source spell checker
Group:                   Utility
Version:                 0.60.6.1
URL:		         http://aspell.net
Source:		         http://ftp.gnu.org/gnu/%srcname/%srcname-%version.tar.gz
License: 		 GPL
SUNW_Copyright:          SFEaspell.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#BuildRequires:      SFEgcc
Requires:           SFEgccruntime

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

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export LIBS="-lm"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --datarootdir=%{_datadir}           \
            --disable-wide-curses

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_includedir}
%{_includedir}/aspell.h
%{_includedir}/pspell/pspell.h
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libaspell.*
%{_libdir}/libpspell.*
%{_libdir}/aspell-*/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/locale/*/LC_MESSAGES/%{srcname}.mo
%{_datadir}/info/%{srcname}*.info

%changelog
* Wed Feb 22 2012- logan@gedanken.org
- Initial spec.
