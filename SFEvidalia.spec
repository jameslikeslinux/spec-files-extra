# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include stdcxx.inc

%define	src_name	vidalia

Name:		SFEvidalia
IPS_Package_Name:	desktop/security/vidalia
Summary:	The Onion Router GUI
Version:	0.2.15
URL:		http://www.torproject.org/
Source:		%{url}/dist/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:		vidalia-01-floor.diff
Patch2:		vidalia-02-max.diff
License:	GPLv2+
Group:		Applications/Internet
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
%include default-depend.inc
Requires:	SFEtor
BuildRequires:	SFEqt-stdcxx-devel
Requires:	SFEqt-stdcxx
BuildRequires:	SFEcmake

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export PATH=/usr/stdcxx/bin:$PATH
export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -library=no%Cstd -I%{stdcxx_include} -I/usr/stdcxx/include"
export LDFLAGS="%_ldflags -lsocket -lnsl -L%{stdcxx_lib} -R%{stdcxx_lib} -L/usr/stdcxx/lib -R/usr/stdcxx/lib -lstdcxx4 -Wl,-zmuldefs"

mkdir -p build && cd build && cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} .. && make -j$CPUS

%install
rm -rf %{buildroot}
cd build && make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_bindir}
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/%{src_name}.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/%{src_name}.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/%{src_name}.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/%{src_name}.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64/apps
%{_datadir}/icons/hicolor/64x64/apps/%{src_name}.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128/apps
%{_datadir}/icons/hicolor/128x128/apps/%{src_name}.png
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/%{src_name}.desktop

%changelog
* Sat Feb 11 2012 - Milan Jurik
- Initial spec
