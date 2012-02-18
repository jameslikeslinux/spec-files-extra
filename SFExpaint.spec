# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name xpaint

Name:		SFExpaint
IPS_Package_Name:	image/editor/xpaint
Summary:	a simple paint program for X
Version:	2.9.9
URL:		http://sf-xpaint.sourceforge.net/
Source:		%{sf_download}/sf-xpaint/%{src_name}-%{version}.tar.bz2
Patch1:		xpaint-01-studio.diff
Group:		Applications/Graphics and Imaging
License:	BSD
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
%include default-depend.inc
BuildRequires:	SFElibxaw3dxft-devel
Requires: 	SFElibxaw3dxft
BuildRequires:	SFEopenjpeg-devel
Requires:	SFEopenjpeg

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc


%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

autoreconf
./configure --prefix=%{_prefix}
make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/%{src_name}

%files root
%defattr (-, root, sys)
%{_sysconfdir}/X11

%changelog
* Sat Feb 18 2012 - Milan Jurik
- Initial spec
