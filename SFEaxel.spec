#
# spec file for package: axel
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): axel
#

%include Solaris.inc

Name:		SFEaxel
Summary:      	HTTP/FTP download manager 
Version:       	2.4
License:	GPL
Url: 		http://axel.alioth.debian.org/
Source:	 	http://alioth.debian.org/frs/download.php/3015/axel-2.4.tar.gz
Group:		Applications/Accessories
Distribution:   OpenSolaris
Vendor:		OpenSolaris Community
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   %{_basedir}
%include default-depend.inc

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name

%description
Axel tries to accelerate HTTP/FTP downloading process by using multiple connections for one file. It can use multiple mirrors for a download. Axel has no dependencies and is lightweight, so it might be useful as a wget clone on byte-critical systems. 

%prep
%setup -q -n axel-%{version}

%build
./configure --prefix=%{_prefix}
sed 's/-Wall //' Makefile > Makefile.fixed
mv Makefile.fixed Makefile
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%attr (0755, root, bin) %{_bindir}/axel
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%{_mandir}

%files root
%defattr (-, root, sys)
%dir %attr (-, root, sys) %{_sysconfdir}
%attr (-, root, root) %{_sysconfdir}/axelrc

%changelog
* Sun Apr 10 2010 - nbprash.mit@gmail.com
- Initial setup.
