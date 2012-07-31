#
# spec file for package SFEdictd
#
# includes module(s): dictd
#
%include Solaris.inc
%define srcname		 dictd

Name:                    SFEdictd
IPS_package_name:        service/network/dictd
Group:                   System/Services
Summary:                 DICTD Server and Client
Version:                 1.12.0
URL:                     http://www.dict.org/w/software/start
License:		 GPLv2+ and LGPLv2+
SUNW_Copyright:          dictd.copyright
Source:                  %sf_download/project/dict/%srcname/%srcname-%version/%srcname-%version.tar.gz
Patch1:			 dictd-01-Makefile.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu
BuildRequires: SFElibmaa-devel
Requires: SFElibmaa

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name


%prep
%setup -q -n dictd-%version
%patch1 -p1

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \

# Use libxnet instead of libsocket
sed 's/-lnsl -lsocket/-lxnet -lnsl/' Makefile > Makefile.xnet
mv Makefile.xnet Makefile

gmake


%install
rm -rf %buildroot
gmake install DESTDIR=$RPM_BUILD_ROOT
rmdir %buildroot%_libdir
mkdir $RPM_BUILD_ROOT%_sysconfdir
echo "server dict.org" > $RPM_BUILD_ROOT%_sysconfdir/dict.conf

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%_bindir
%_sbindir
%dir %attr(0755, root, sys) %_datadir
%_mandir
%_includedir

%files root
%defattr (-, root, sys)
%attr (-, root, root) %{_sysconfdir}/dict.conf


%changelog
* Sat Dec 17 2011 - Alex Viskovatoff
- Fix directory attributes
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Tue Jan 25 2011 - Alex Viskovatoff
- Update to 1.12.0
* Jun 19 2010 - pradhap (at) gmail.com
- Fixed URL
* Mar 29 2008 - pradhap (at) gmail.com
- Initial dictd spec file.
