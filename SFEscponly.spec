# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name scponly

Name:		SFEscponly
IPS_Package_Name:	network/scponly
Summary:	an alternative 'shell' (of sorts) for ssh
Version:	4.8
URL:		https://github.com/scponly/scponly/wiki
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tgz
Group:		Applications/Graphics and Imaging
License:	GPLv2+
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
%include default-depend.inc

%description
an alternative 'shell' (of sorts) for system administrators who would like to provide access to remote users to both read and write local files without providing any remote execution priviledges.

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}	\
	--enable-scp-compat	\
	--enable-rsync-compat	\
	--enable-winscp-compat

make -j$CPUS

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{src_name} %{buildroot}%{_bindir}/%{src_name}
mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 %{src_name}.8 %{buildroot}%{_mandir}/man1/%{src_name}.1

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Fri Apr 13 2012 - Milan Jurik
- Initial spec
