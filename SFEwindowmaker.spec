#
# spec file for package SFEwindowmaker
#
#
%include Solaris.inc

Name:		SFEwindowmaker
IPS_Package_Name:	desktop/window-manager/windowmaker
Summary:	Windowmaker Your Next Window Manager
Version:	0.92.0
Source:		http://windowmaker.org/pub/source/release/WindowMaker-%{version}.tar.bz2
Source1:	windowmaker.desktop
URL:		http://www.windowmaker.info/ 
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWcsu
Requires: %name-root

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
Requires: %name

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
%setup -q -n WindowMaker-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
	--enable-modelock	\
	--disable-static

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/xsessions && cp %{SOURCE1} %{buildroot}%{_datadir}/xsessions/

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr(0755, root, bin) %{_libdir}
%dir %attr(0755, root, bin) %{_libdir}/locale
%{_libdir}/lib*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr(0755, root, bin) %{_datadir}/WindowMaker
%{_datadir}/WindowMaker/*
%dir %attr(0755, root, bin) %{_datadir}/WPrefs
%{_datadir}/WPrefs/*
%dir %attr(0755, root, bin) %{_datadir}/WINGs
%{_datadir}/WINGs/*
%{_datadir}/xsessions/windowmaker.desktop

%files root
%defattr (-, root, sys)
%dir %attr (-, root, sys) %_sysconfdir
%_sysconfdir/WindowMaker

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%changelog
* Sun Feb 15 2012 - Milan Jurik
- package reorganization
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Fixed directory attributes
- Fri Dec 12 2007 - pradhap (at) gmail.com
- Initial Windowmaker spec file

