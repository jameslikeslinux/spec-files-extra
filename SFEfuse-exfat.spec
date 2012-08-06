#
# spec file for package SFEfuse-exfat
#
#
# you will need FUSE see: http://www.opensolaris.org/os/project/fuse

%include Solaris.inc

%include base.inc

%define SFEscons         %(/usr/bin/pkg info scons >/dev/null 2>&1 && echo 0 || echo 1)
%define SUNWlibfuse      %(/usr/bin/pkginfo -q SUNWlibfuse && echo 1 || echo 0)

Name:                    SFEfuse-exfat
IPS_Package_Name:	system/file-system/fuse-exfat
Summary:                 Free exFAT file system implementation
Version:                 0.9.6
License:                 GPLv3
SUNW_copyright:          fuse-exfat.copyright
Source:			 http://exfat.googlecode.com/files/fuse-exfat-%{version}.tar.gz
Url:                     http://code.google.com/p/exfat/
Group:		System/File System
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%if %SFEscons
BuildRequires: SFEscons
%endif

%if %SUNWlibfuse
BuildRequires:  SUNWlibfuse
Requires:       SUNWfusefs
Requires:       SUNWlibfuse
%else
BuildRequires:  SFElibfuse
Requires:       SFEfusefs
Requires:       SFElibfuse
%endif

%prep
%setup -q -n fuse-exfat-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export CPPPATH="/usr/include/fuse"

scons -j $CPUS CC="$CC" CFLAGS="$CFLAGS" CPPPATH="$CPPPATH"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/fs/exfat
mkdir -p $RPM_BUILD_ROOT%{_mandir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man/man8
#cp fsck/exfatck $RPM_BUILD_ROOT%{_sbindir}
cp fuse/mount.exfat-fuse $RPM_BUILD_ROOT%{_sbindir}
cp fuse/mount.exfat-fuse.8 $RPM_BUILD_ROOT%{_mandir}/man/man8
ln -s %{_sbindir}/mount.exfat-fuse $RPM_BUILD_ROOT%{_libdir}/fs/exfat/mount
#ln -s %{_sbindir}/exfatck $RPM_BUILD_ROOT%{_libdir}/fs/exfat/fsck
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/exfat
%{_libdir}/fs/exfat/*
%{_mandir}/man/man8/*.8

%changelog
* Mon Feb 13 2012 - Ken Mays <kmays2000@gmail.com>
- Bumped to 0.9.6
* Tue Nov 1 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to 0.9.5
- Tested on oi_151 and libfuse 20100615
* Tue Sep 27 2011 - Alex Viskovatoff
- Add SUNW_copyright
* Fri Sep 21 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.9.2, drop upstreamed patches
- Support SFEfusefs
* Fri Jun 18 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
