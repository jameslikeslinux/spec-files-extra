#
# spec file for package SFEntfs-3g
#
#
# you will need FUSE see: http://www.opensolaris.org/os/project/fuse

%include Solaris.inc
%include base.inc

Name:                    SFEfuse-ext2
IPS_Package_Name:	 system/file-system/fuse-ext2 
Summary:                 fuse ext2 filesystem (ext2fs/ext3fs) driver
Version:                 0.0.7
License:                 GPLv2
SUNW_copyright:          fuse-ext2.copyright
Source:			 %{sf_download}/fuse-ext2/fuse-ext2-%{version}.tar.gz
Patch1:			 fuse-ext2-0.0.7-01-sunpro.diff
Patch2:			 fuse-ext2-0.0.7-02-solaris.diff
Patch3:			 fuse-ext2-0.0.7-03-readdir.diff
Patch4:                  fuse-ext2-0.0.7-04-ifhwaddr.diff
Url:                     http://alperakcan.org/?open=projects&project=fuse-ext2
Group:		System/File System
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
%define _execprefix %{_prefix}

BuildRequires: SFElibfuse-devel
Requires: SFElibfuse

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWlibfuse

%prep
%setup -q -n fuse-ext2-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1 
%patch4 -p0

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

#export CC="/usr/sfw/bin/gcc"
#export CFLAGS="%gcc_optflags"
export CFLAGS="%optflags -xc99"
export LDFLAGS="%{_ldflags}"

./autogen.sh
./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}                 \
	    --mandir=%{_mandir}                 \
            --sysconfdir=%{_sysconfdir}         \
	    --datadir=%{_datadir}               \
            --bindir=%{_bindir}                 \
            --includedir=%{_includedir}         \
            --exec-prefix=%{_execprefix}

# avoid building unused parts of e2fsprogs that need porting
make -j $CPUS -C e2fsprogs*/et
make -j $CPUS -C e2fsprogs*/ext2fs
make -j $CPUS -C fuse-ext2

%install
rm -rf $RPM_BUILD_ROOT
make -C fuse-ext2 install DESTDIR=$RPM_BUILD_ROOT
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc README ChangeLog COPYING AUTHORS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}

%changelog
* Mon Feb 13 2012 - Ken Mays <kmays2000@gmail.com> 
- Bump to 0.0.7
* Tue Sep 27 2011 - Alex Viskovatoff
- Add SUNW_copyright
* Sun Jun 21 2009 - trisk@forkgnu.org
- Initial spec
