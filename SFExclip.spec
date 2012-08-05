#
# spec file for package SFExclip
#
# includes module(s): xclip
#
%include Solaris.inc

Name:		SFExclip
IPS_Package_Name:	x11/library/xclip
Summary:	Command line interface to the X11 clipboard
Group:		System/X11
Version:	0.12
Source:		%{sf_download}/xclip/xclip/%{version}/xclip-%{version}.tar.gz
URL:		http://sourceforge.net/projects/xclip/
License:	GPL
SUNW_Copyright:	xclip.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWxwplt 
Requires: SUNWxwplt 

%description
xclip is a command line interface to the X11 clipboard. It can also be used for copying files, as an alternative to sftp/scp, thus avoiding password prompts when X11 forwarding has already been setup.

%prep
%setup -q -n xclip-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags" # -I/usr/X11/include"
export LDFLAGS="%_ldflags" # -L/usr/X11/lib -R/usr/X11/lib"

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}	

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr (-, root, bin)
%doc COPYING ChangeLog README
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Mon Jul 25 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Sat Jun 18 2011 - Thomas Wagner
- fix permissions for %{_datadir}/doc
* Mon Jun 13 2011 - Thomas Wagner
- Initial spec
