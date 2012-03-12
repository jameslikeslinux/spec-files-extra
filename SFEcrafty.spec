#
# spec file for package SFEcrafty
#
# includes module(s): crafty
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:		SFEcrafty
IPS_Package_Name:	games/crafty
Summary:	Crafty chess engine  
Version:	23.4
Group:		Amusements/Games
URL:		http://www.craftychess.com/
Source:		http://www.craftychess.com/crafty-%{version}.zip
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n crafty-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

make -j $CPUS target=SUN crafty-make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mv crafty %{buildroot}/%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}

%changelog
* Mon Mar 12 2012 - Milan Jurik
- fix build with newer gcc
* Mon Feb 07 2011 - Milan Jurik
- bump to 23.4
* May 2010 - Gilles Dauphin
- %files update, move to %_bindir
* Sun May 09 2010 - Milan Jurik
- update to 23.2
* Wed Apr 15 2009 - Alexander R. Eremin eremin@milax.org
- Initial spec file.
