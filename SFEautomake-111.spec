#
# spec file for package SFEautomake-111
#
# includes module(s): automake
#
%include Solaris.inc

Name:		SFEautomake-111
IPS_Package_Name:	developer/build/automake-111
Summary:	GNU Automake 1.11
License:	GPLv2
URL:		http://http://www.gnu.org/software/automake/
Version:	1.11.1
Source:		http://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n automake-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_bindir}/aclocal
rm -f %{buildroot}/%{_bindir}/automake
rm -rf %{buildroot}/%{_infodir}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/aclocal-1.11
%{_datadir}/automake-1.11
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_mandir}

%changelog
* Tue Oct 11 2011 - Milan Jurik
- Initial spec
