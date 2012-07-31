#
# spec file for package SFEaaphoto
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:		SFEaaphoto
IPS_Package_Name:	image/editor/aaphoto
Summary:	Auto Adjust Photo, automatic color correction of photos
Version:	0.41
Group:		Applications/Graphics and Imaging
URL:		http://log69.com/aaphoto.html
License:	GPLv3
Source:		http://log69.com/downloads/aaphoto_sources_v%{version}.tar.gz
Patch1:		aaphoto-01-ccopenmp.diff
SUNW_Copyright:	%{name}.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEjasper-devel
Requires: SFEjasper
BuildRequires: SUNWzlib
Requires: SUNWzlib
BuildRequires: SUNWjpg-devel
Requires: SUNWjpg
BuildRequires: SUNWpng-devel
Requires: SUNWpng

%prep
%setup -q -n aaphoto-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS 

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%{_bindir}

%changelog
* Mon Oct 17 2011 - Milan Jurik
- add IPS package name
* Mon Jul 11 2011 - Guido Berhoerster
- added copyright file
* Fri Feb 04 2011 - Milan Jurik
- bump to 0.41
* Sun Dec 26 2010 - Milan Jurik
- Initial spec file
