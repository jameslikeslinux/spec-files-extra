#
# spec file for package SFEtea
#
# includes module(s): tea
#
%include Solaris.inc
%include stdcxx.inc

Name:		SFEtea
IPS_Package_Name:	editor/tea
Summary:	Powerful text editor
Version:	31.2.0
License:	GPLv2
Group:		Development/Editors
URL:		http://tea-editor.sourceforge.net/
Source:		%{sf_download}/tea-editor/tea-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEqt-stdcxx-devel
Requires: SFEqt-stdcxx

%description
TEA is a very small, but powerful text editor with many unique features.

%prep
%setup -q -n tea-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH=/usr/stdcxx/bin:$PATH
export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -library=no%Cstd -I%{stdcxx_include} -I/usr/stdcxx/include"
export LDFLAGS="%_ldflags -L%{stdcxx_lib} -R%{stdcxx_lib} -L/usr/stdcxx/lib -R/usr/stdcxx/lib -lstdcxx4 -Wl,-zmuldefs"

qmake
make -j$CPUS

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp bin/tea %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}

%changelog
* Mon Feb 06 2012 - Milan Jurik
- unfortunately GTK version is dead, bump to 31.2.0 based on QT
* Tue Aug  7 2007 - dougs@truemail.co.th
- Bump to 17.1.4
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
