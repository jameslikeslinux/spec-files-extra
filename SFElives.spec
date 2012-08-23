#
# spec file for package SFElives.spec
#
# includes module(s): lives
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	LiVES
%define src_url		http://www.xs4all.nl/~salsaman/lives/current

Name:		SFElives
IPS_Package_Name:	video/editor/lives
License:	GPL v3
Summary:	Video Editing System
Version:	1.6.1
URL:		http://lives.sourceforge.net/
Group:		Applications/Sound and Video
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch7:		lives-07-solaris.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:	SFEmplayer
BuildRequires:	SUNWjpg-devel
Requires:	SUNWjpg
BuildRequires:	SUNWsound-exchange
Requires:	SUNWsound-exchange
Requires:	SUNWimagick
Requires:	SFEmjpegtools

%prep
%setup -q -n lives-%{version}
%patch7 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++

LDFLAGS="-lsocket -lresolv -lnsl"	\
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_bindir}/lives
cd $RPM_BUILD_ROOT/%{_bindir}/ && ln -s lives-exe lives
cd $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%{_datadir} && mv locale/nl_NL locale/nl && mv locale/de_DE locale/de

rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/app-install
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_datadir}/lives
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*so*
%{_libdir}/lives
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun Apr 01 2012 - Milan Jurik
- bump to 1.6.1
* Sat May 29 2010 - Milan Jurik
- update to 1.3.3, remove patch applied by upstream
* Mon Mar 08 2010 - Milan Jurik
- update to 1.2.1, removed patches applied by upstream
* Sat Jan 16 2010 - Milan Jurik
- update to 1.1.8
* Fri Sep 18 2009 - Milan Jurik
- Initial version
