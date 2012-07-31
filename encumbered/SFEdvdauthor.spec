#
# spec file for package SFEdvdauthor
#
# includes module(s): SFEdvdauthor
#
%include Solaris.inc

Name:		SFEdvdauthor
IPS_Package_Name:	video/dvdauthor
Summary:	dvdauthor a program that will generate a DVD movie
Version:	0.7.0
Source:		%{sf_download}/dvdauthor/dvdauthor-%{version}.tar.gz
Patch2:		dvdauthor-02-wall.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibdvdnav
BuildRequires: SFElibdvdnav-devel
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel

%prep
%setup -q -n dvdauthor
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export MSGFMT="/usr/bin/msgfmt"

autoreconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_bindir}/*
%{_datadir}/*

%changelog
* Sun Mar 11 2012 - Milan Jurik
- bump to 0.7.0
* Fri Aug 21 2009 - Milan Jurik
- update to 0.6.14
* Thu Aug 07 2008 - trisk@acm.jhu.edu
- Rename SFElibdvdread dependency to SFElibdvdnav
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
